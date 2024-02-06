import json
import os
from unittest.mock import ANY, MagicMock, call
from urllib.parse import quote

import pytest
from bitbucketcli.bitbucket.repository import RepositoryCommand


@pytest.mark.parametrize(
    "workspace,name,project_key,is_private,status_code",
    [
        ("workspace1", "repository1", "projectkey1", True, 200),
        ("workspace2", "repository2", "projectkey2", False, 200),
        ("workspace3", "repository3", "projectkey3", True, 200),
    ],
)
def test_create_repository(
    mock_session, workspace, name, project_key, is_private, status_code
):
    repository_create_url = f"{api_repositories_url()}/{workspace}/{name}"
    branch_restriction_url = (
        f"{api_repositories_url()}/{workspace}/{name}/branch-restrictions"
    )

    create_repository_payload = json.dumps(
        {
            "scm": "git",
            "project": {"key": project_key},
            "is_private": is_private,
            "name": name,
        }
    )
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    create_repository_mock = MagicMock(name="create_repository_mock")
    create_repository_mock.status_code = status_code
    create_repository_mock.json.return_value = {"mainbranch": {"name": "master"}}

    push_restriction_mock = MagicMock(name="push_restriction_mock")
    force_restriction_mock = MagicMock(name="force_restriction_mock")
    delete_restriction_mock = MagicMock(name="delete_restriction_mock")

    push_restriction_payload = json.dumps(restriction_payload("push"))
    force_restriction_payload = json.dumps(restriction_payload("force"))
    delete_restriction_payload = json.dumps(restriction_payload("delete"))

    payloads = [
        create_repository_mock,
        push_restriction_mock,
        force_restriction_mock,
        delete_restriction_mock,
    ]
    mock_session.post.side_effect = payloads

    repository = RepositoryCommand(workspace, mock_session)
    create_result = repository.create(name, project_key, is_private)
    assert create_result is True
    assert mock_session.post.call_count == 4
    mock_session.post.assert_has_calls(
        [
            call(
                url=repository_create_url,
                data=create_repository_payload,
                headers=headers,
                params=None,
            ),
            call(
                url=branch_restriction_url,
                data=push_restriction_payload,
                headers=headers,
                params=None,
            ),
            call(
                url=branch_restriction_url,
                data=force_restriction_payload,
                headers=headers,
                params=None,
            ),
            call(
                url=branch_restriction_url,
                data=delete_restriction_payload,
                headers=headers,
                params=None,
            ),
        ]
    )


@pytest.mark.parametrize(
    "workspace,name,project_key,is_private,status_code",
    [
        ("workspace1", "repository1", "projectkey1", True, 400),
        ("workspace2", "repository2", "projectkey2", False, 400),
        ("workspace3", "repository3", "projectkey3", True, 400),
        ("workspace1", "repository1", "projectkey1", True, 401),
        ("workspace2", "repository2", "projectkey2", False, 401),
        ("workspace3", "repository3", "projectkey3", True, 401),
    ],
)
def test_fail_to_create_repository(
    mock_session, workspace, name, project_key, is_private, status_code
):
    repository_create_url = f"{api_repositories_url()}/{workspace}/{name}"

    create_repository_payload = json.dumps(
        {
            "scm": "git",
            "project": {"key": project_key},
            "is_private": is_private,
            "name": name,
        }
    )

    create_repository_mock = MagicMock()
    create_repository_mock.status_code = status_code

    payloads = [
        create_repository_mock,
    ]
    mock_session.post.side_effect = payloads

    repository = RepositoryCommand(workspace, mock_session)
    create_result = repository.create(name, project_key, is_private)
    assert create_result is False
    mock_session.post.assert_called_with(
        url=repository_create_url,
        data=create_repository_payload,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        params=None,
    )


@pytest.mark.parametrize(
    "workspace,email,repository_name,permission,status_code",
    [
        ("workspace1", "fancyemail@email.com", "repository1", "admin", 200),
        ("workspace2", "fancyemail@email.com", "repository2", "write", 200),
        ("workspace3", "fancyemail@email.com", "repository3", "read", 200),
        ("workspace1", "fancyemail@email.com", "repository1", "read", 200),
        ("workspace2", "fancyemail@email.com", "repository2", "write", 200),
        ("workspace3", "fancyemail@email.com", "repository3", "admin", 200),
    ],
)
def test_add_user_with_success(
    workspace, email, repository_name, permission, status_code
):
    url = f"{internal_api_url()}/\u0021api/internal/invitations/repositories/{workspace}/{repository_name}"
    session_mock = MagicMock()
    session_mock.post.return_value.status_code = status_code
    repository = RepositoryCommand(workspace, session_mock)
    result = repository.add_user_to_repository(email, repository_name, permission)
    payload = {"emails": [email], "permission": permission}
    assert result is True
    session_mock.post.assert_called_with(
        url=url,
        data=json.dumps(payload),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        params=ANY,
    )


@pytest.mark.parametrize(
    "workspace,email,repository_name,permission,status_code",
    [
        ("workspace1", "fancyemail@email.com", "repository1", "admin", 400),
        ("workspace2", "fancyemail@email.com", "repository2", "write", 400),
        ("workspace3", "fancyemail@email.com", "repository3", "read", 400),
        ("workspace1", "fancyemail@email.com", "repository1", "read", 400),
        ("workspace2", "fancyemail@email.com", "repository2", "write", 400),
        ("workspace3", "fancyemail@email.com", "repository3", "admin", 400),
    ],
)
def test_fail_to_add_user(workspace, email, repository_name, permission, status_code):
    url = f"{internal_api_url()}/\u0021api/internal/invitations/repositories/{workspace}/{repository_name}"
    session_mock = MagicMock()
    session_mock.post.return_value.status_code = status_code
    repository = RepositoryCommand(workspace, session_mock)
    result = repository.add_user_to_repository(email, repository_name, permission)
    payload = {"emails": [email], "permission": permission}
    assert result is False
    session_mock.post.assert_called_with(
        url=url,
        data=json.dumps(payload),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        params=ANY,
    )


@pytest.mark.parametrize(
    "workspace,account_id,repository_name,status_code",
    [
        (
            "workspace1",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository1",
            204,
        ),
        (
            "workspace2",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository2",
            204,
        ),
        (
            "workspace3",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository3",
            204,
        ),
        (
            "workspace1",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository1",
            204,
        ),
        (
            "workspace2",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository2",
            204,
        ),
        (
            "workspace3",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository3",
            204,
        ),
    ],
)
def test_remove_user_with_success(
    mocker, workspace, account_id, repository_name, status_code
):
    uuid = "{3333333-444444444-444444-44444}"
    mocker.patch(
        "bitbucketcli.bitbucket.bitbucket.BitbucketClient.get_user_uuid",
        return_value=uuid,
    )
    session_mock = MagicMock()
    session_mock.delete.return_value.status_code = status_code

    repository = RepositoryCommand(workspace, session_mock)
    result = repository.remove_user_from_repository(repository_name, account_id)
    url = f"{internal_api_url()}/\u0021api/internal/privileges/{workspace}/{repository_name}/{quote(uuid)}"
    assert result is True
    assert session_mock.delete.call_count == 1
    session_mock.delete.assert_called_with(
        url=url, headers={"Accept": "application/json"}, params=None, data=None
    )


@pytest.mark.parametrize(
    "workspace,account_id,repository_name,status_code",
    [
        (
            "workspace1",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository1",
            400,
        ),
        (
            "workspace2",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository2",
            400,
        ),
        (
            "workspace3",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository3",
            410,
        ),
        (
            "workspace1",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository1",
            400,
        ),
        (
            "workspace2",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository2",
            410,
        ),
        (
            "workspace3",
            "616030:07848922-j1ee-57f0-acd3-6c7677078h96",
            "repository3",
            400,
        ),
    ],
)
def test_fail_to_remove_user(
    mocker, workspace, account_id, repository_name, status_code
):
    uuid = "{3333333-444444444-444444-44444}"
    mocker.patch(
        "bitbucketcli.bitbucket.bitbucket.BitbucketClient.get_user_uuid",
        return_value=uuid,
    )
    session_mock = MagicMock()
    session_mock.delete.return_value.status_code = status_code

    repository = RepositoryCommand(workspace, session_mock)
    result = repository.remove_user_from_repository(repository_name, account_id)
    url = f"{internal_api_url()}/\u0021api/internal/privileges/{workspace}/{repository_name}/{quote(uuid)}"
    assert result is False
    assert session_mock.delete.call_count == 1
    session_mock.delete.assert_called_with(
        url=url, headers={"Accept": "application/json"}, params=None, data=None
    )


def internal_api_url():
    return os.getenv("BITBUCKET_INTERNAL_API_URL")


def api_repositories_url():
    return f"{os.getenv('BITBUCKET_API_URL')}/2.0/repositories"


def restriction_payload(kind):
    return {
        "type": "branchrestriction",
        "kind": kind,
        "branch_match_kind": "glob",
        "pattern": "master",
        "users": [],
        "groups": [],
    }
