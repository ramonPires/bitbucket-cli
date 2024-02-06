from urllib.parse import quote

from bitbucketcli.bitbucket.bitbucket import BitbucketClient


class WorkspaceCommand(BitbucketClient):
    def remove_user_from_group(self, workspace, account_id, group_name):
        uuid = super().get_user_uuid(account_id)
        response = super().delete(
            f"1.0/groups/{workspace}/{group_name}/members/{quote(uuid)}"
        )
        return response.status_code == 204
