import pytest
from bitbucketcli.bitbucket import cli


@pytest.mark.parametrize(
    "workspace,repository,branch",
    [
        ("workspace1", "repository1", "master"),
        ("workspace2", "repository2", "main"),
        ("workspace3", "repository1", "master"),
    ],
)
def test_bypass_push_with_pull_request_with_success(
    runner, mock_client, workspace, repository, branch
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.branch.BranchCommand.bypass_push_with_pull_request",
        return_value=True,
    )
    result = runner.invoke(
        cli.enable_bypass_branch_pull_request,
        ["--workspace", workspace, "--repository", repository, "--branch", branch],
    )
    mock.assert_called_once_with(branch)
    output = f"Branch bypass pull request was enabled with success for repository {repository}"
    assert result.exit_code == 0
    assert result.output == f"{output}\n"


@pytest.mark.parametrize(
    "workspace,repository,branch",
    [
        ("workspace1", "repository1", "master"),
        ("workspace2", "repository2", "main"),
        ("workspace3", "repository1", "master"),
    ],
)
def test_fail_bypass_push_with_pull_request(
    runner, mock_client, workspace, repository, branch
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.branch.BranchCommand.bypass_push_with_pull_request",
        return_value=False,
    )
    result = runner.invoke(
        cli.enable_bypass_branch_pull_request,
        ["--workspace", workspace, "--repository", repository, "--branch", branch],
    )
    mock.assert_called_once_with(branch)
    output = f"Error: Failed to enable branch bypass pull request for repository {repository}"
    assert result.exit_code == 0
    assert result.output == f"{output}\n"
