from unittest.mock import MagicMock

import pytest
import requests
from click.testing import CliRunner


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="function")
def mock_client(mocker):
    mocker.patch(
        "requests_oauthlib.oauth2_session.OAuth2Session.fetch_token",
        return_value="fake_token",
    )
    mocker.patch(
        "bitbucketcli.bitbucket.cli.prepare_oauth_client", return_value=MagicMock()
    )
    return mocker


@pytest.fixture(scope="function")
def mock_session(mocker):
    mock = mocker.patch.object(requests, "Session", autospec=True)
    mock.return_value.__enter__.return_value = mock
    return mock
