import os
from unittest.mock import MagicMock, call

import pytest
from bitbucketcli.bitbucket.branch import BranchCommand


@pytest.mark.parametrize(
    "workspace,repository,branch,status_code",
    [
        ("workspace1", "repository1", "master", 204),
        ("workspace2", "repository2", "main", 204),
        ("workspace3", "repository1", "master", 204),
    ],
)
def test_bypass_push_with_pull_request_with_success(
    workspace, repository, branch, status_code
):
    restriction_id = "1234"
    remove_push_restriction = (
        f"{restriction_api_url(workspace, repository)}/{restriction_id}"
    )

    session_mock = MagicMock()
    session_mock.get.return_value.json.return_value = {
        "values": [{"id": restriction_id}]
    }
    session_mock.delete.return_value.status_code = status_code

    command = BranchCommand(workspace, repository, session_mock)
    result = command.bypass_push_with_pull_request(branch)

    assert result is True
    assert session_mock.get.call_count == 1
    assert session_mock.delete.call_count == 1
    session_mock.get.assert_called_with(
        url=restriction_api_url(workspace, repository),
        data=None,
        headers={"Accept": "application/json"},
        params={"kind": "push", "pattern": branch},
    )
    session_mock.delete.assert_called_with(
        url=remove_push_restriction,
        data=None,
        headers={"Accept": "application/json"},
        params=None,
    )


@pytest.mark.parametrize(
    "workspace,repository,status_code",
    [
        ("workspace1", "repository1", 204),
        ("workspace2", "repository2", 204),
        ("workspace3", "repository1", 204),
    ],
)
def test_bypass_push_with_pull_request_default_branch_with_success(
    workspace, repository, status_code
):
    restriction_id = "1234"
    default_branch_url = repositories_api_url(workspace, repository)
    remove_push_restriction_url = (
        f"{restriction_api_url(workspace, repository)}/{restriction_id}"
    )
    default_branch_name = "master"
    session_mock = MagicMock()

    get_default_branch_mock = MagicMock(name="get_default_branch_mock")
    get_default_branch_mock.json.return_value = {
        "mainbranch": {"name": default_branch_name}
    }

    get_branch_restriction_mock = MagicMock(name="get_branch_restriction_mock")
    get_branch_restriction_mock.json.return_value = {"values": [{"id": restriction_id}]}

    session_mock.get.side_effect = [
        get_default_branch_mock,
        get_branch_restriction_mock,
    ]

    session_mock.delete.return_value.status_code = status_code

    command = BranchCommand(workspace, repository, session_mock)
    result = command.bypass_push_with_pull_request()

    assert result is True
    assert session_mock.get.call_count == 2
    assert session_mock.delete.call_count == 1

    session_mock.get.assert_has_calls(
        [
            call(
                url=default_branch_url,
                data=None,
                headers={"Accept": "application/json"},
                params=None,
            ),
            call(
                url=restriction_api_url(workspace, repository),
                data=None,
                headers={"Accept": "application/json"},
                params={"kind": "push", "pattern": default_branch_name},
            ),
        ]
    )
    session_mock.delete.assert_called_with(
        url=remove_push_restriction_url,
        data=None,
        headers={"Accept": "application/json"},
        params=None,
    )


@pytest.mark.parametrize(
    "workspace,repository,branch,status_code",
    [
        ("workspace1", "repository1", "master", 400),
        ("workspace2", "repository2", "main", 410),
        ("workspace3", "repository1", "master", 400),
    ],
)
def test_fail_to_bypass_push_with_pull_request(
    workspace, repository, branch, status_code
):
    restriction_id = "1234"
    remove_push_restriction = (
        f"{restriction_api_url(workspace, repository)}/{restriction_id}"
    )

    session_mock = MagicMock()
    session_mock.get.return_value.json.return_value = {
        "values": [{"id": restriction_id}]
    }
    session_mock.delete.return_value.status_code = status_code

    command = BranchCommand(workspace, repository, session_mock)
    result = command.bypass_push_with_pull_request(branch)

    assert result is False
    assert session_mock.get.call_count == 1
    assert session_mock.delete.call_count == 1
    session_mock.get.assert_called_with(
        url=restriction_api_url(workspace, repository),
        data=None,
        headers={"Accept": "application/json"},
        params={"kind": "push", "pattern": branch},
    )
    session_mock.delete.assert_called_with(
        url=remove_push_restriction,
        data=None,
        headers={"Accept": "application/json"},
        params=None,
    )


@pytest.mark.parametrize(
    "workspace,repository,branch",
    [
        ("workspace1", "repository1", "master"),
        ("workspace2", "repository2", "main"),
        ("workspace3", "repository1", "master"),
    ],
)
def test_fail_to_bypass_push_with_pull_request_if_push_restriction_dont_exists(
    workspace, repository, branch
):
    session_mock = MagicMock()
    session_mock.get.return_value.json.return_value = {"values": []}

    command = BranchCommand(workspace, repository, session_mock)
    result = command.bypass_push_with_pull_request(branch)

    assert result is False
    assert session_mock.get.call_count == 1
    assert session_mock.delete.call_count == 0
    session_mock.get.assert_called_with(
        url=restriction_api_url(workspace, repository),
        data=None,
        headers={"Accept": "application/json"},
        params={"kind": "push", "pattern": branch},
    )


def restriction_api_url(workspace, repository):
    return f"{repositories_api_url(workspace, repository)}/branch-restrictions"


def repositories_api_url(workspace, repository):
    return f"{os.getenv('BITBUCKET_API_URL')}/2.0/repositories/{workspace}/{repository}"
