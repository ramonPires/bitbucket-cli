from unittest.mock import MagicMock

import pytest
from bitbucketcli.bitbucket import cli


@pytest.mark.parametrize(
    "workspace,name,key,description,is_private",
    [
        ("workspace1", "project1", "projectkey1", "description1", "--public"),
        ("workspace2", "project2", "projectkey2", "description2", "--private"),
    ],
)
def test_create_project_with_success(
    runner, mock_client, workspace, name, key, description, is_private
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.project.ProjectCommand.create", return_value=True
    )

    result = runner.invoke(
        cli.create_project,
        [
            "--workspace",
            workspace,
            "--name",
            name,
            "--key",
            key,
            is_private,
            "--description",
            description,
        ],
    )
    visibility = {"--public": False, "--private": True}
    mock.assert_called_once_with(name, key, visibility[is_private], description)
    output = f"Project created with success. You can access here: https://bitbucket.org/{workspace}/workspace/projects/{key}"
    assert result.exit_code == 0
    assert result.output == f"{output}\n"


@pytest.mark.parametrize(
    "workspace,name,key,description,is_private",
    [
        ("workspace1", "project1", "projectkey1", "description1", "--public"),
        ("workspace2", "project2", "projectkey2", "description2", "--private"),
    ],
)
def test_create_project_failure(
    runner, mock_client, workspace, name, key, description, is_private
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.project.ProjectCommand.create", return_value=False
    )
    result = runner.invoke(
        cli.create_project,
        [
            "--workspace",
            workspace,
            "--name",
            name,
            "--key",
            key,
            is_private,
            "--description",
            description,
        ],
    )
    visibility = {"--public": False, "--private": True}
    mock.assert_called_once_with(name, key, visibility[is_private], description)
    assert result.exit_code == 0
    assert result.output == "Error: Project failed to create.\n"
