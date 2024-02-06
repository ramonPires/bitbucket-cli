import pytest
from bitbucketcli.bitbucket import cli


@pytest.mark.parametrize(
    "workspace,email,repository,permission",
    [
        ("workspace1", "fancyemail@email.com", "repository1", "read"),
        ("workspace2", "fancyemail2@email.com", "repository2", "write"),
        ("workspace3", "fancyemail3@email.com", "repository1", "admin"),
    ],
)
def test_add_user_to_repository_with_success(
    runner, mock_client, workspace, email, repository, permission
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.add_user_to_repository",
        return_value=True,
    )
    result = runner.invoke(
        cli.add_user_to_repository,
        [
            "--workspace",
            workspace,
            "--email",
            email,
            "--repository",
            repository,
            "--permission",
            permission,
        ],
    )
    mock.assert_called_once_with(email, repository, permission)
    output = f"Invite to access the repository {repository} was created with success for user with email {email}"
    assert result.exit_code == 0
    assert result.output == f"{output}\n"


@pytest.mark.parametrize(
    "workspace,email,repository,permission",
    [
        ("workspace1", "fancyemail@email.com", "repository1", "read"),
        ("workspace2", "fancyemail2@email.com", "repository2", "write"),
        ("workspace3", "fancyemail3@email.com", "repository1", "admin"),
    ],
)
def test_fail_to_add_user_to_repository(
    runner, mock_client, workspace, email, repository, permission
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.add_user_to_repository",
        return_value=False,
    )
    result = runner.invoke(
        cli.add_user_to_repository,
        [
            "--workspace",
            workspace,
            "--email",
            email,
            "--repository",
            repository,
            "--permission",
            permission,
        ],
    )
    mock.assert_called_once_with(email, repository, permission)
    output = f"Error: Failed to invite to access the repository {repository} for user with email {email}."
    assert result.exit_code == 0
    assert result.output == f"{output}\n"


@pytest.mark.parametrize(
    "workspace,email,repository,permission",
    [
        ("workspace1", "fancyemail#email.com", "repository1", "read"),
        ("workspace2", "fancyemail2@email.com)", "repository2", "write"),
        ("workspace3", "$fancyemail3@email.com", "repository1", "admin"),
        ("workspace3", "$fancyemail3xemail.com", "repository1", "admin"),
        ("workspace3", "$f3xemail.com", "repository1", "write"),
    ],
)
def test_fail_to_add_user_to_repository_with_invalid_email(
    runner, mock_client, workspace, email, repository, permission
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.add_user_to_repository"
    )
    result = runner.invoke(
        cli.add_user_to_repository,
        [
            "--workspace",
            workspace,
            "--email",
            email,
            "--repository",
            repository,
            "--permission",
            permission,
        ],
    )
    assert mock.call_count == 0
    output = f"Error: Invalid value for '--email': E-mail \"{email}\" format invalid."
    assert result.exit_code != 0
    assert output in result.output


##


@pytest.mark.parametrize(
    "workspace,name,project_key,is_private",
    [
        ("workspace1", "repository1", "projectkey1", "--public"),
        ("workspace2", "repository2", "projectkey2", "--private"),
    ],
)
def test_create_repository_with_success(
    runner, mock_client, workspace, name, project_key, is_private
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.create", return_value=True
    )
    result = runner.invoke(
        cli.create_repository,
        [
            "--workspace",
            workspace,
            "--name",
            name,
            "--project-key",
            project_key,
            is_private,
        ],
    )
    visibility = {"--public": False, "--private": True}
    mock.assert_called_once_with(name, project_key, visibility[is_private])
    assert result.exit_code == 0
    assert (
        result.output
        == f"Repository created with success. You can access here: https://bitbucket.org/{workspace}/{name}/src\n"
    )


@pytest.mark.parametrize(
    "workspace,name,project_key,is_private",
    [
        ("workspace1", "repository1", "projectkey1", "--public"),
        ("workspace2", "repository2", "projectkey2", "--private"),
    ],
)
def test_fail_to_create_repository(
    runner, mock_client, workspace, name, project_key, is_private
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.create", return_value=False
    )
    result = runner.invoke(
        cli.create_repository,
        [
            "--workspace",
            workspace,
            "--name",
            name,
            "--project-key",
            project_key,
            is_private,
        ],
    )
    visibility = {"--public": False, "--private": True}
    mock.assert_called_once_with(name, project_key, visibility[is_private])
    assert result.exit_code == 0
    assert result.output == f"Error: Repository failed to create.\n"


@pytest.mark.parametrize(
    "workspace,account_id,repository",
    [
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "repository1"),
        ("workspace2", "616045:07848922-j1ee-57f0-acd3-6c7677078h96", "repository2"),
    ],
)
def test_remove_user_from_repository_with_success(
    runner, mock_client, workspace, account_id, repository
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.remove_user_from_repository",
        return_value=True,
    )
    result = runner.invoke(
        cli.remove_user_from_repository,
        [
            "--workspace",
            workspace,
            "--account-id",
            account_id,
            "--repository",
            repository,
        ],
    )
    output = f"User with account id {account_id} removed with success from repository {repository}"
    mock.assert_called_once_with(repository, account_id)
    assert result.exit_code == 0
    assert result.output == f"{output}\n"


@pytest.mark.parametrize(
    "workspace,account_id,repository",
    [
        ("workspace1", "616030:07848922-j1ee-57f0-acd3-6c7677078h96", "repository1"),
        ("workspace2", "616045:07848922-j1ee-57f0-acd3-6c7677078h96", "repository2"),
    ],
)
def test_fail_to_remove_user_from_repository(
    runner, mock_client, workspace, account_id, repository
):
    mock = mock_client.patch(
        "bitbucketcli.bitbucket.repository.RepositoryCommand.remove_user_from_repository",
        return_value=False,
    )
    result = runner.invoke(
        cli.remove_user_from_repository,
        [
            "--workspace",
            workspace,
            "--account-id",
            account_id,
            "--repository",
            repository,
        ],
    )
    output = f"Error: Failed to remove ser with account id {account_id} from repository {repository}"
    mock.assert_called_once_with(repository, account_id)
    assert result.exit_code == 0
    assert result.output == f"{output}\n"
