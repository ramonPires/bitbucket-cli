import pytest
from bitbucketcli.bitbucket import cli


@pytest.mark.parametrize(
    "workspace,account_id,group",
    [
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "group1"),
        ("workspace2", "616045:07848922-j1ee-57f0-acd3-6c7677078h96", "group2"),
    ],
)
def test_remove_user_from_group_with_success(
    runner, mock_client, workspace, account_id, group
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.workspace.WorkspaceCommand.remove_user_from_group",
        return_value=True,
    )

    result = runner.invoke(
        cli.remove_user_from_group,
        ["--workspace", workspace, "--account-id", account_id, "--group", group],
    )
    mock.assert_called_once_with(workspace, account_id, group)
    output = (
        f"User with account id {account_id} removed with success from the group {group}"
    )
    assert result.exit_code == 0
    assert result.output == f"{output}\n"


@pytest.mark.parametrize(
    "workspace,account_id,group",
    [
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "group1"),
        ("workspace2", "616045:07848922-j1ee-57f0-acd3-6c7677078h96", "group2"),
    ],
)
def test_fail_to_remove_user_from_group(
    runner, mock_client, workspace, account_id, group
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.workspace.WorkspaceCommand.remove_user_from_group",
        return_value=False,
    )

    result = runner.invoke(
        cli.remove_user_from_group,
        ["--workspace", workspace, "--account-id", account_id, "--group", group],
    )
    mock.assert_called_once_with(workspace, account_id, group)
    output = f"Error: Failed to remove user with account id {account_id} from the group {group}"
    assert result.exit_code == 0
    assert result.output == f"{output}\n"
