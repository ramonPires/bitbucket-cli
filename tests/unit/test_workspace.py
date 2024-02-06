import os
from unittest.mock import MagicMock
from urllib.parse import quote

import pytest
from bitbucketcli.bitbucket.workspace import WorkspaceCommand


@pytest.mark.parametrize(
    "workspace,account_id,group_name,status_code",
    [
        (
            "workspace1",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "developers",
            204,
        ),
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "admin", 204),
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "qa", 204),
    ],
)
def test_remove_user_from_group_with_success(
    mocker, workspace, account_id, group_name, status_code
):
    uuid = "{3333333-444444444-444444-44444}"
    url = f"{api_groups_url()}/{workspace}/{group_name}/members/{quote(uuid)}"
    mocker.patch(
        "bitbucketcli.bitbucket.bitbucket.BitbucketClient.get_user_uuid",
        return_value=uuid,
    )
    session_mock = MagicMock()
    session_mock.delete.return_value.status_code = status_code
    command = WorkspaceCommand(session_mock)
    result = command.remove_user_from_group(workspace, account_id, group_name)
    assert result is True
    assert session_mock.delete.call_count == 1
    session_mock.delete.assert_called_with(
        url=url, headers={"Accept": "application/json"}, params=None, data=None
    )


@pytest.mark.parametrize(
    "workspace,account_id,group_name,status_code",
    [
        (
            "workspace1",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "developers",
            400,
        ),
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "admin", 400),
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "qa", 400),
    ],
)
def test_fail_remove_user_from_group(
    mocker, workspace, account_id, group_name, status_code
):
    uuid = "{3333333-444444444-444444-44444}"
    url = f"{api_groups_url()}/{workspace}/{group_name}/members/{quote(uuid)}"
    mocker.patch(
        "bitbucketcli.bitbucket.bitbucket.BitbucketClient.get_user_uuid",
        return_value=uuid,
    )
    session_mock = MagicMock()
    session_mock.delete.return_value.status_code = status_code
    command = WorkspaceCommand(session_mock)
    result = command.remove_user_from_group(workspace, account_id, group_name)
    assert result is False
    assert session_mock.delete.call_count == 1
    session_mock.delete.assert_called_with(
        url=url, headers={"Accept": "application/json"}, params=None, data=None
    )


def api_groups_url():
    return f"{os.getenv('BITBUCKET_API_URL')}/1.0/groups"
