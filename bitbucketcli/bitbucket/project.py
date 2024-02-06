import json

from bitbucketcli.bitbucket.bitbucket import BitbucketClient


class ProjectCommand(BitbucketClient):
    def __init__(self, workspace, oauth_client):
        super().__init__(oauth_client)
        self.__workspace = workspace

    def create(self, name, key, is_private=True, description=""):
        payload = {
            "name": name,
            "key": key,
            "description": description,
            "is_private": is_private,
        }
        dump = json.dumps(payload)
        response = super().post(
            f"2.0/workspaces/{self.__workspace}/projects", data=dump
        )
        return response.status_code == 201
