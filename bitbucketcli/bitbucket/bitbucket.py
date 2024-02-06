import logging
from os import getenv

import requests


class BitbucketApiException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"{self.status_code} - Request failed from Bitbucket Api"


class BitbucketClient:
    def __init__(self, oauth_client):
        self.__api_url = getenv("BITBUCKET_API_URL")
        self.__internal_api_url = getenv("BITBUCKET_INTERNAL_API_URL")
        self.__oauth = oauth_client

    def post(self, path, data, headers=None, is_internal_api=False):
        return self.__request(
            self.__oauth.post,
            path=path,
            data=data,
            headers=headers
            or {"Accept": "application/json", "Content-Type": "application/json"},
            is_internal_api=is_internal_api,
        )

    def get(self, path, params=None, headers=None, is_internal_api=False):
        return self.__request(
            self.__oauth.get,
            path=path,
            params=params,
            headers=headers
            or {
                "Accept": "application/json",
            },
            is_internal_api=is_internal_api,
        )

    def delete(self, path, params=None, headers=None, is_internal_api=False):
        return self.__request(
            self.__oauth.delete,
            path=path,
            params=params,
            headers=headers
            or {
                "Accept": "application/json",
            },
            is_internal_api=is_internal_api,
        )

    def __request(
        self,
        requests_func,
        path,
        data=None,
        params=None,
        headers=None,
        is_internal_api=False,
    ):
        if headers is None:
            headers = {"Accept": "application/json"}
        try:
            url = f"{self.__get_url(is_internal_api)}/{path}"
            response = requests_func(url=url, data=data, params=params, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            logging.error("Failed to process request, error=%{e.response.text}")
            raise e

    def __get_url(self, is_internal_api):
        return self.__internal_api_url if is_internal_api else self.__api_url

    def get_user_uuid(self, account_id):
        user_response = self.get(f"2.0/users/{account_id}")
        if user_response.status_code == 200:
            return user_response.json()["uuid"]

        raise BitbucketApiException(
            f"Failed to fetch user with account id {account_id}",
            status_code=user_response.status_code,
        )
