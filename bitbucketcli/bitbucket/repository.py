import json
from urllib.parse import quote

from bitbucketcli.bitbucket.bitbucket import BitbucketClient


class RepositoryCommand(BitbucketClient):
    def __init__(self, workspace, oauth_client):
        super().__init__(oauth_client)
        self.__workspace = workspace

    def create(self, name, project_key, is_private=True):
        payload = {
            "scm": "git",
            "project": {"key": project_key},
            "is_private": is_private,
            "name": name,
        }
        dump = json.dumps(payload)
        new_repository_response = self.post(
            f"2.0/repositories/{self.__workspace}/{name}", data=dump
        )
        if new_repository_response.status_code == 200:
            main_branch = new_repository_response.json()["mainbranch"]["name"]
            self.__apply_default_branch_restrictions(name, main_branch)
            return True
        return False

    def add_user_to_repository(self, email, repository_name, permission="read"):
        path = f"\u0021api/internal/invitations/repositories/{self.__workspace}/{repository_name}"
        dump = json.dumps({"emails": [email], "permission": permission})
        response = super().post(path=path, data=dump, is_internal_api=True)
        return response.status_code == 200

    def remove_user_from_repository(self, repository_name, account_id):
        uuid = self.get_user_uuid(account_id)
        path = f"\u0021api/internal/privileges/{self.__workspace}/{repository_name}/{quote(uuid)}"
        response = super().delete(path=path, is_internal_api=True)
        return response.status_code == 204

    def __apply_default_branch_restrictions(self, repository_name, branch_name):
        for kind in ["push", "force", "delete"]:
            self.__apply_restriction(kind, repository_name, branch_name)

    def __apply_restriction(self, kind, repository_name, branch_name):
        data = {
            "type": "branchrestriction",
            "kind": kind,
            "branch_match_kind": "glob",
            "pattern": branch_name,
            "users": [],
            "groups": [],
        }
        dump = json.dumps(data)
        super().post(
            f"2.0/repositories/{self.__workspace}/{repository_name}/branch-restrictions",
            data=dump,
        )
