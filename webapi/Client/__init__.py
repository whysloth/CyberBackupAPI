import sys
import traceback

import webapi.endpoints as endpoints
import requests
import time
import typing


def exception_handling(method: typing.Callable):
    """
    Handling some common errors. Connection errors and 401 (re-auth).

    :param method: typing.Callable
    :return a result of called method:
    """

    def inner(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)

        except requests.ConnectionError:
            sys.stderr.write(traceback.format_exc())
            sys.stderr.write("Connection error.")

        except requests.HTTPError as e:
            if e.response.status_code == 401:
                self.auth()
                return method(self, *args, **kwargs)
            else:
                raise

        except Exception:
            sys.stderr.write(traceback.format_exc())
            sys.stderr.write("Unknown error during authentication process. ")
            raise

    return inner


class Client:
    def __init__(self, username: str, password: str):
        self.__token_info = {}
        self.__username = username
        self.__password = password

        self._next_auth_time = 0.0

        try:
            self.auth()

        except requests.ConnectionError:
            sys.stderr.write("Unable to connect.")

        except Exception:
            raise

    def auth(self):
        """
        Authenticate a client with provided credentials.
        :return: None
        """
        auth_payload = endpoints.AUTH_PAYLOAD.copy()
        auth_payload["password"] = self.__password
        auth_payload["username"] = self.__username

        auth_time = time.time()
        resp = requests.post(endpoints.AUTH_URL, auth_payload)
        resp.raise_for_status()

        if resp.ok:
            self.__token_info = resp.json()
            self._next_auth_time = auth_time + self.__token_info["expires_in"]

    @exception_handling
    def alerts_summary(self, is_active: None | str = None, order_by: None | str = None, order_type: None | str = None):
        """
        Lists all alerts from the system.

        :param is_active: str | None
        :param order_by: str | None
        :param order_type: str | None
        :return: dict
        """
        alerts_summary_headers = endpoints.AUTHORIZATION_TOKEN_HEADER.copy()
        alerts_summary_headers["Authorization"] += self.__token

        alerts_summary_payload = {}

        if is_active is not None:
            alerts_summary_payload["is_active"] = is_active

        if order_by is not None:
            alerts_summary_payload["order_by"] = order_by

        if order_type is not None:
            alerts_summary_payload["order_type"] = order_type

        resp = requests.get(endpoints.ALERTS_SUMMARY_URL, headers=alerts_summary_headers, data=alerts_summary_payload)
        resp.raise_for_status()

        if resp.ok:
            return resp.json()

    @exception_handling
    def daily_activity_table(self, _from: str | None = None, order_by: str | None = None, order_type: str | None = None,
                             limit: int | None = None):
        """
        Lists all resource-related daily activities with extra details

        :param _from: str | None
        :param order_by: str | None
        :param order_type: str | None
        :param limit: int | None
        :return: dict
        """
        daily_activity_table_headers = endpoints.AUTHORIZATION_TOKEN_HEADER.copy()
        daily_activity_table_headers["Authorization"] += self.__token

        daily_activity_table_payload = {}

        if _from is not None:
            daily_activity_table_payload["from"] = _from
        if order_by is not None:
            daily_activity_table_payload["order_by"] = order_by
        if order_type is not None:
            daily_activity_table_payload["order_type"] = order_type
        if limit is not None:
            daily_activity_table_payload["limit"] = limit

        resp = requests.get(endpoints.DAILY_ACTIVITY_TABLE_URL, headers=daily_activity_table_headers,
                            data=daily_activity_table_payload)
        resp.raise_for_status()

        if resp.ok:
            return resp.json()

    @exception_handling
    def active_alerts_table(self, order_type: str | None = None, order_by: str | None = None, limit: int | None = None):
        """
        Lists all active alerts with extra info.

        :param order_type: str | None
        :param order_by: str | None
        :param limit: int | None
        :return: dict
        """
        active_alerts_table_headers = endpoints.AUTHORIZATION_TOKEN_HEADER.copy()
        active_alerts_table_headers["Authorization"] += self.__token

        active_alerts_table_payload = {}

        if order_by is not None:
            active_alerts_table_payload["order_by"] = order_by
        if order_type is not None:
            active_alerts_table_payload["order_type"] = order_type
        if limit is not None:
            active_alerts_table_payload["limit"] = limit

        resp = requests.get(endpoints.ACTIVE_ALERTS_TABLE_URL, headers=active_alerts_table_headers,
                            data=active_alerts_table_payload)
        resp.raise_for_status()

        if resp.ok:
            return resp.json()

    @exception_handling
    def resource_summary_table(self, _from: str | None = None, limit: int | None = None):
        """
        List all protected resources with extra info.

        :param _from: str | None
        :param limit: int | None
        :return: dict
        """
        resource_summary_table_headers = endpoints.AUTHORIZATION_TOKEN_HEADER.copy()
        resource_summary_table_headers["Authorization"] += self.__token

        resource_summary_table_payload = {}

        if _from is not None:
            resource_summary_table_payload["from"] = _from
        if limit is not None:
            resource_summary_table_payload["limit"] = limit

        resp = requests.get(endpoints.RESOURCE_SUMMARY_TABLE_URL, headers=resource_summary_table_headers,
                            data=resource_summary_table_payload)
        resp.raise_for_status()

        if resp.ok:
            return resp.json()

    @exception_handling
    def location_summary_table(self, _from: str | None = None, limit: int | None = None):
        """
        Lists all storages with extra info.

        :param _from: str | None
        :param limit: int | None
        :return: dict
        """
        location_summary_table_headers = endpoints.AUTHORIZATION_TOKEN_HEADER.copy()
        location_summary_table_headers["Authorization"] += self.__token

        location_summary_table_payload = {}

        if _from is not None:
            location_summary_table_payload["from"] = _from
        if limit is not None:
            location_summary_table_payload["limit"] = limit

        resp = requests.get(endpoints.LOCATION_SUMMARY_TABLE_URL, headers=location_summary_table_headers,
                            data=location_summary_table_payload)
        resp.raise_for_status()

        if resp.ok:
            return resp.json()

    @property
    def __token(self):
        try:
            return self.__token_info["access_token"]
        except KeyError:
            return None


__all__ = [Client]
