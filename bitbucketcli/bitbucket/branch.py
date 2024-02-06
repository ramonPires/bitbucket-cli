from bitbucketcli.bitbucket.bitbucket import BitbucketClient


class BranchCommand(BitbucketClient):
    def __init__(self, workspace, repository, oauth_client):
        super().__init__(oauth_client)
        self.__workspace = workspace
        self.__repository = repository

    def bypass_push_with_pull_request(self, branch_name=None):
        branch = branch_name if branch_name else self.__get_default_branch()
        restriction_id = self.__get_push_restriction_id(branch)
        if restriction_id:
            result = self.__remove_restriction(restriction_id)
            return result.status_code == 204
        return False

    def __get_default_branch(self):
        repository_response = super().get(
            f"2.0/repositories/{self.__workspace}/{self.__repository}"
        )
        repository = repository_response.json()
        return repository["mainbranch"]["name"]

    def __get_push_restriction_id(self, branch_name):
        restrictions_response = super().get(
            f"2.0/repositories/{self.__workspace}/{self.__repository}/branch-restrictions",
            params={"kind": "push", "pattern": branch_name},
        )
        values = restrictions_response.json()["values"]
        if len(values) != 0:
            return values[0]["id"]
        return None

    def __remove_restriction(self, restriction_id):
        return super().delete(
            f"2.0/repositories/{self.__workspace}/{self.__repository}/branch-restrictions/{restriction_id}"
        )
