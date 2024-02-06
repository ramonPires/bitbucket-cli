import json
import os
from unittest.mock import ANY, MagicMock

import pytest
from bitbucketcli.bitbucket.project import ProjectCommand


@pytest.mark.parametrize(
    "workspace,name,key,description,is_private,status_code,created",
    [
        ("workspace1", "project1", "projectkey1", "description1", True, 201, True),
        ("workspace2", "project2", "projectkey2", "description2", False, 201, True),
        ("workspace3", "project3", "projectkey3", "", True, 201, True),
        ("workspace1", "project1", "projectkey1", "description1", True, 400, False),
        ("workspace2", "project2", "projectkey2", "description2", False, 400, False),
        ("workspace3", "project3", "projectkey3", "", True, 400, False),
    ],
)
def test_create_project(
    workspace, name, key, description, is_private, status_code, created
):
    session_mock = MagicMock()
    session_mock.post.return_value.status_code = status_code
    project = ProjectCommand(workspace, session_mock)
    create_result = project.create(name, key, is_private, description)
    payload = {
        "name": name,
        "key": key,
        "description": description,
        "is_private": is_private,
    }
    url = f"{os.getenv('BITBUCKET_API_URL')}/2.0/workspaces/{workspace}/projects"
    assert create_result is created
    session_mock.post.assert_called_with(
        url=url,
        data=json.dumps(payload),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        params=ANY,
    )
