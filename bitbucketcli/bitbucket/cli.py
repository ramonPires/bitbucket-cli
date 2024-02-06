import re
from os import getenv

import click
from bitbucketcli.bitbucket.branch import BranchCommand
from bitbucketcli.bitbucket.project import ProjectCommand
from bitbucketcli.bitbucket.repository import RepositoryCommand
from bitbucketcli.bitbucket.workspace import WorkspaceCommand
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def validate_email(ctx, param, value):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, value):
        return value

    raise click.BadParameter(f'E-mail "{value}" format invalid.')


def prepare_oauth_client():
    client_id = getenv("BITBUCKET_OAUTH_CONSUMER_KEY")
    client_secret = getenv("BITBUCKET_OAUTH_CONSUMER_SECRET")
    token_url = getenv("BITBUCKET_TOKEN_URL")
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(
        token_url=token_url, client_id=client_id, client_secret=client_secret
    )
    return oauth


@click.group()
def cli():
    """A command line tool to access bitbucket cloud functionalities."""


@cli.command(short_help="Create a new project in a specific workspace.")
@click.option(
    "--workspace",
    prompt="Workspace name",
    type=click.STRING,
    help="Workspace name where the project belongs",
)
@click.option("--name", prompt="Project name", type=click.STRING, help="Project name")
@click.option("--key", prompt="Project key", type=click.STRING, help="Project key")
@click.option(
    "--description",
    prompt="Project Description",
    default="",
    type=click.STRING,
    help="Project description",
)
@click.option("--private/--public", is_flag=True, show_default=True, default=True)
def create_project(workspace, name, key, description, private):
    project = ProjectCommand(workspace, prepare_oauth_client())
    created = project.create(name, key, private, description)
    if created:
        click.echo(
            f"Project created with success. You can access here: https://bitbucket.org/{workspace}/workspace/projects/{key}"
        )
    else:
        click.ClickException("Project failed to create.").show()


@cli.command(short_help="Create a new repository in a specific project.")
@click.option(
    "--workspace",
    prompt="Workspace name",
    type=click.STRING,
    help="Workspace name where the project belongs",
)
@click.option(
    "--name", prompt="Repository name", type=click.STRING, help="Project name"
)
@click.option(
    "--project-key", prompt="Project key", type=click.STRING, help="Project key"
)
@click.option("--private/--public", is_flag=True, show_default=True, default=True)
def create_repository(workspace, name, project_key, private):
    """Create a new repository in a specific project."""
    repository = RepositoryCommand(workspace, prepare_oauth_client())
    created = repository.create(name, project_key, private)
    if created:
        click.echo(
            f"Repository created with success. You can access here: https://bitbucket.org/{workspace}/{name}/src"
        )
    else:
        click.ClickException("Repository failed to create.").show()


@cli.command(
    short_help="Add the user to a repository. An email with the invite will be sent to the user by default."
)
@click.option(
    "--workspace",
    prompt="Workspace name",
    type=click.STRING,
    help="Workspace name where the repository belongs",
)
@click.option(
    "--email",
    prompt="User email",
    type=click.STRING,
    callback=validate_email,
    help="User email",
)
@click.option(
    "--repository", prompt="Repository name", type=click.STRING, help="Repository name"
)
@click.option(
    "--permission",
    type=click.Choice(["read", "write", "admin"], case_sensitive=False),
    default="read",
    prompt="User permission",
    help="Permission of the user inside of the repository",
)
def add_user_to_repository(workspace, email, repository, permission):
    command = RepositoryCommand(workspace, prepare_oauth_client())
    if command.add_user_to_repository(email, repository, permission):
        click.echo(
            f"Invite to access the repository {repository} was created with success for user with email {email}"
        )
    else:
        click.ClickException(
            f"Failed to invite to access the repository {repository} for user with email {email}."
        ).show()


@cli.command(short_help="Remove a user from a repository.")
@click.option(
    "--workspace",
    prompt="Workspace name",
    type=click.STRING,
    help="Workspace name where the repository belongs",
)
@click.option(
    "--account-id",
    prompt="Account ID",
    type=click.STRING,
    help="Account ID - You can obtain your account id here: https://id.atlassian.com/gateway/api/me",
)
@click.option(
    "--repository", prompt="Repository name", type=click.STRING, help="Repository name"
)
def remove_user_from_repository(workspace, account_id, repository):
    command = RepositoryCommand(workspace, prepare_oauth_client())
    if command.remove_user_from_repository(repository, account_id):
        click.echo(
            f"User with account id {account_id} removed with success from repository {repository}"
        )
    else:
        click.ClickException(
            f"Failed to remove ser with account id {account_id} from repository {repository}"
        ).show()


@cli.command(short_help="Enable users to use push force in a branch.")
@click.option(
    "--workspace",
    prompt="Workspace name",
    type=click.STRING,
    help="Workspace name where the repository belongs",
)
@click.option(
    "--repository",
    prompt="Repository name",
    type=click.STRING,
    help="Repository name",
)
@click.option(
    "--branch",
    prompt="Branch name",
    prompt_required=False,
    default=None,
    type=click.STRING,
    help="Branch name, if not defined, the default branch will be used",
)
def enable_bypass_branch_pull_request(workspace, repository, branch):
    command = BranchCommand(workspace, repository, prepare_oauth_client())
    if command.bypass_push_with_pull_request(branch):
        click.echo(
            f"Branch bypass pull request was enabled with success for repository {repository}"
        )
    else:
        click.ClickException(
            f"Failed to enable branch bypass pull request for repository {repository}"
        ).show()


@cli.command(short_help="Remove a user from a group in a workspace.")
@click.option(
    "--workspace",
    prompt="Workspace name",
    type=click.STRING,
    help="Workspace name where the user group belongs",
)
@click.option(
    "--account-id",
    prompt="Account ID",
    type=click.STRING,
    help="Account ID - You can obtain your account id here: https://id.atlassian.com/gateway/api/me",
)
@click.option("--group", prompt="Group name", type=click.STRING, help="Group name")
def remove_user_from_group(workspace, account_id, group):
    workspace_command = WorkspaceCommand(prepare_oauth_client())
    if workspace_command.remove_user_from_group(workspace, account_id, group):
        click.echo(
            f"User with account id {account_id} removed with success from the group {group}"
        )
    else:
        click.ClickException(
            f"Failed to remove user with account id {account_id} from the group {group}"
        ).show()
