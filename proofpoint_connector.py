# File: proofpoint_connector.py
#
# Copyright (c) 2017-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
import json
import sys
from datetime import datetime, timedelta

import phantom.app as phantom
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from proofpoint_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class ProofpointConnector(BaseConnector):
    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._pp_conn = None
        self._state_file_path = None
        self._state = {}

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        self._username = config["username"]
        self._password = config["password"]
        self._headers = {"X-Requested-With": "REST API", "Content-type": "application/json", "Accept": "application/json"}

        return phantom.APP_SUCCESS

    def finalize(self):
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def _get_error_message_from_exception(self, e):
        """This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_message = e.args[1]
                elif len(e.args) == 1:
                    error_code = ERROR_CODE_MESSAGE
                    error_message = e.args[0]
            else:
                error_code = ERROR_CODE_MESSAGE
                error_message = ERROR_MESSAGE_UNAVAILABLE
        except:
            error_code = ERROR_CODE_MESSAGE
            error_message = ERROR_MESSAGE_UNAVAILABLE

        try:
            if error_code not in ERROR_CODE_MESSAGE:
                error_text = ERROR_MESSAGE_FORMAT_WITHOUT_CODE.format(error_message)
            else:
                error_text = ERROR_MESSAGE_FORMAT_WITH_CODE.format(error_code, error_message)
        except:
            self.debug_print(PARSE_ERROR_MESSAGE)
            error_text = PARSE_ERROR_MESSAGE

        return error_text

    def _validate_integer(self, action_result, parameter, key):
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    return action_result.set_status(phantom.APP_ERROR, INVALID_INTEGER_ERROR_MESSAGE.format(key)), None

                parameter = int(parameter)
            except:
                return action_result.set_status(phantom.APP_ERROR, INVALID_INTEGER_ERROR_MESSAGE.format(key)), None

            if parameter < 0:
                return action_result.set_status(phantom.APP_ERROR, INVALID_NON_NEGATIVE_INTEGER_ERROR_MESSAGE.format(key)), None

        return phantom.APP_SUCCESS, parameter

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, EMPTY_RESPONSE_MESSAGE.format(response.status_code)), None)

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = ("\n").join(split_lines)
        except:
            error_text = HTML_RESPONSE_PARSE_ERROR_MESSAGE

        message = SERVER_ERROR_MESSAGE.format(status_code, error_text)
        message = message.replace("{", "{{").replace("}", "}}")
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, JSON_PARSE_ERROR_MESSAGE.format(error_message)), None)
        else:
            if 200 <= r.status_code < 399:
                return RetVal(phantom.APP_SUCCESS, resp_json)

        message = None

        # Check for message in error
        if resp_json.get("message"):
            message = SERVER_ERROR_MESSAGE.format(r.status_code, resp_json["message"])

        if not message:
            error_message = r.text.replace("{", "{{").replace("}", "}}")
            message = SERVER_ERROR_MESSAGE.format(r.status_code, error_message)
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately
        if not r.ok:
            return self._process_html_response(r, action_result)

        # Process a json response
        if "json" in r.headers.get("Content-Type", ""):
            return self._process_json_response(r, action_result)

        # Process an HTML response
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        error_message = r.text.replace("{", "{{").replace("}", "}}")
        message = SERVER_ERROR_CANT_PROCESS_RESPONSE_MESSAGE.format(r.status_code, error_message)
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, action_result, endpoint, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        resp_json = None

        # Create a URL to connect to
        url = f"{PP_API_BASE_URL}{endpoint}"

        self._auth = (self._username, self._password)

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), resp_json)

        try:
            res = request_func(url, auth=self._auth, headers=self._headers, **kwargs)
        except requests.exceptions.ConnectionError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, CONNECTION_REFUSED_ERROR_MESSAGE), resp_json)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, SERVER_CONNECTION_ERROR_MESSAGE.format(error_message)), resp_json)

        return self._process_response(res, action_result)

    def _process_clicks(self, clicks, action):
        for click in clicks:
            guid = click.pop("GUID")
            self.save_progress(f"Processing click {guid}")
            container = {
                "start_time": click.get("threatTime"),
                "name": "{} event {}".format(click.get("classification"), action),
                "source_data_identifier": guid,
                "artifacts": [],
            }
            artifacts = container["artifacts"]

            # pull these out for consistency with messages
            email_addresses = {"sender": click.pop("sender"), "recipient": click.pop("recipient")}

            cef = click
            cef["sourceAddress"] = cef.get("clickIP")
            cef["requestURL"] = cef.get("url")
            cef["action"] = action
            cef_types = {
                "campaignId": ["proofpoint campaign id"],
                "clickIP": ["ip"],
                "recipient": ["email"],
                "sender": ["email"],
                "threatID": ["proofpoint threat id"],
                "threatURL": ["url"],
                "url": ["url"],
            }
            artifacts.append(
                {
                    "name": f"click {action} event",
                    "cef": cef,
                    "cef_types": cef_types,
                    "label": "event",
                    "source_data_identifier": 0,
                    "run_automation": False,
                }
            )

            count = 1
            for key in email_addresses:
                if email_addresses[key] is not None:
                    artifacts.append(
                        {
                            "name": "email artifact",
                            "cef": {key: email_addresses[key]},
                            "cef_types": {key: ["email"]},
                            "label": "event",
                            "source_data_identifier": count,
                            "run_automation": False,
                        }
                    )
                    count += 1

            artifacts[-1]["run_automation"] = True

            self.save_container(container)

    def _process_messages(self, messages, action):
        for message in messages:
            guid = message.pop("GUID")
            self.save_progress(f"Processing message {guid}")
            container = {
                "start_time": message.get("messageTime"),
                "name": f"Message event {action}",
                "source_data_identifier": guid,
                "artifacts": [],
            }
            artifacts = container["artifacts"]

            threats = message.pop("threatsInfoMap", [])
            email_addresses = {
                "ccAddress": message.pop("ccAddresses", []),
                "fromAddress": message.pop("fromAddress", []),
                "recipient": message.pop("recipient", []),
                "replyToAddress": message.pop("replyToAddress", []),
                "toAddress": message.pop("toAddresses", []),
                "sender": message.pop("sender", []),
            }
            for key in email_addresses:
                if not isinstance(email_addresses[key], list):
                    email_addresses[key] = [email_addresses[key]]

            # first add an artifact of all the base data
            cef = message
            cef["sourceAddress"] = cef.get("senderIP")
            cef["action"] = action
            cef["modulesRun"] = ", ".join(cef["modulesRun"])
            cef["policyRoutes"] = ", ".join(cef["policyRoutes"])

            cef_types = {
                "senderIP": ["ip"],
            }
            artifact = {
                "name": "message event",
                "cef": cef,
                "cef_types": cef_types,
                "label": "event",
                "source_data_identifier": 0,
                "run_automation": False,
            }

            artifacts.append(artifact)

            count = 1
            for threat in threats:
                cef = threat
                cef_types = {"campaignId": ["proofpoint campaign id"], "threatId": ["proofpoint threat id"], "threatUrl": ["url"]}
                threat_type = cef.get("threatType").lower()
                if threat_type == "url":
                    cef_types["threat"] = ["url"]
                    cef["requestURL"] = cef.get("threat")
                elif threat_type == "attachment":
                    cef_types["threat"] = ["hash", "sha256"]
                    cef["fileHash"] = cef.get("threat")
                elif threat_type == "messagetext":
                    cef_types["threat"] = ["email"]
                    cef["fromEmail"] = cef.get("threat")

                artifact = {
                    "name": "threat detail",
                    "cef": cef,
                    "cef_types": cef_types,
                    "label": "event",
                    "source_data_identifier": count,
                    "run_automation": False,
                }
                count += 1
                artifacts.append(artifact)

            for key in email_addresses:
                for item in email_addresses[key]:
                    artifacts.append(
                        {
                            "name": "email artifact",
                            "cef": {key: item},
                            "cef_types": {key: ["email"]},
                            "label": "event",
                            "source_data_identifier": count,
                            "run_automation": False,
                        }
                    )
                    count += 1

            artifacts[-1]["run_automation"] = True

            self.save_container(container)

    def _on_poll(self, param):
        action_result = self.add_action_result(ActionResult(param))
        if self.is_poll_now():
            self.save_progress(
                "Due to the nature of the API, the container "
                "and artifact limits imposed by POLL NOW are "
                "ignored. As a result POLL NOW will simply "
                "resume where the previous ingestion activity "
                "stopped and attempt to import all available "
                "containers and artifacts."
            )

        # The API only allows for the last 12 hours to be accessible, and they
        # must be polled in no more than one hour intervals. Since this is very
        # much a real time service and playing catch-up is rather pointless,
        # limit polling to the last hour.

        mins = self.get_config()["initial_ingestion_window"]

        ret_val, mins = self._validate_integer(action_result, mins, INITIAL_INGESTION_WINDOW_KEY)
        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if not (1 <= mins <= 60):
            return action_result.set_status(
                phantom.APP_ERROR, "Asset configuration parameter, 'initial_ingestion_window', must be an integer between 1 and 60"
            )

        start_at = (datetime.utcnow() - timedelta(minutes=mins)).replace(microsecond=0).isoformat() + "Z"

        if not self._state or "last_poll" not in self._state or self._state["last_poll"] < start_at:
            self._state["last_poll"] = start_at

        params = {"sinceTime": self._state["last_poll"], "format": "json"}

        # Connect to the server
        ret_val, data = self._make_rest_call(action_result, PP_API_PATH_ALL, params=params)

        if phantom.is_fail(ret_val):
            if "The sinceTime parameter gives a time too far into the past" in action_result.get_message():
                action_result.append_to_message(
                    "It is possible the Phantom clock has drifted."
                    " Please re-sync it or consider lowering 'initial_ingestion_window' action parameter"
                )
            return action_result.get_status()

        config = self.get_config()
        if config.get("ingest_permitted_clicks", True) and "clicksPermitted" in data:
            self.save_progress("Processing {} permitted clicks".format(len(data["clicksPermitted"])))
            self._process_clicks(data["clicksPermitted"], "permitted")
        if config.get("ingest_blocked_clicks", True) and "clicksBlocked" in data:
            self.save_progress("Processing {} blocked clicks".format(len(data["clicksBlocked"])))
            self._process_clicks(data["clicksBlocked"], "blocked")
        if config.get("ingest_delivered_messages", True) and "messagesDelivered" in data:
            self.save_progress("Processing {} delivered messages".format(len(data["messagesDelivered"])))
            self._process_messages(data["messagesDelivered"], "delivered")
        if config.get("ingest_blocked_messages", True) and "messagesBlocked" in data:
            self.save_progress("Processing {} blocked messages".format(len(data["messagesBlocked"])))
            self._process_messages(data["messagesBlocked"], "blocked")

        self._state["last_poll"] = data["queryEndTime"]

        return self.set_status(phantom.APP_SUCCESS)

    def _test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(param))
        start_at = (datetime.utcnow() - timedelta(minutes=5)).replace(microsecond=0).isoformat() + "Z"

        params = {"sinceTime": start_at, "format": "json"}

        # Connect to the server
        ret_val, _ = self._make_rest_call(action_result, PP_API_PATH_ALL, params=params)
        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_campaign(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        self.debug_print("Redirect to _get_campaign_details function.")
        self._get_campaign_details(param)

    def _get_campaign_details(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(param))
        campaign_id = param.get("campaign_id")

        campaign_url = PP_API_PATH_CAMPAIGN.format(campaign_id)

        params = {"format": "json"}

        ret_val, data = self._make_rest_call(action_result, campaign_url, params=params)
        if phantom.is_fail(ret_val):
            self.debug_print("Failed to get campaign details.")
            return action_result.get_status()

        action_result.add_data(data)
        self.debug_print("successfully to get campaign details.")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_forensic(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        self.debug_print("Redirect to _get_forensic_data function.")
        self._get_forensic_data(param)

    def _get_forensic_data(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(param))
        campaign_id = param.get("campaign_id")
        threat_id = param.get("threat_id")
        include_campaign_forensics = param.get("include_campaign_forensics", False)

        if not campaign_id and not threat_id:
            return action_result.set_status(phantom.APP_ERROR, ("Campaign ID or Threat ID must be specified"))

        if campaign_id and threat_id:
            return action_result.set_status(phantom.APP_ERROR, ("Only one of Campaign ID or Threat ID must be specified"))

        params = {}
        if campaign_id:
            params["campaignId"] = campaign_id
        if threat_id:
            params["threatId"] = threat_id
            if include_campaign_forensics:
                params["includeCampaignForensics"] = include_campaign_forensics
        ret_val, data = self._make_rest_call(action_result, PP_API_PATH_FORENSICS, params=params)
        if phantom.is_fail(ret_val):
            self.debug_print("Failed to get forensic data.")
            return action_result.get_status()

        action_result.add_data(data)
        self.debug_print("successfully get forensic data.")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _decode_url(self, param):
        """This function is used to handle the decoding of a Proofpoint rewritten URL.
        :param param: Dictionary of input parameters
        :return: status success/failure
        """
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        params = {}
        url_list = []
        url = param["url"]

        # The Decode API allows for multiple values. Split the parameter by ,
        url_list = [x.strip() for x in url.split(",")]
        url_list = list(filter(None, url_list))
        if not url_list:
            return action_result.set_status(phantom.APP_ERROR, "Please provide a valid value in the 'url' action parameter")

        # Add the URL(s) to the json
        params["urls"] = url_list

        # Make rest call
        ret_val, response = self._make_rest_call(action_result, PP_API_PATH_DECODE, method="post", json=params)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        """Function that handles all the actions

        Args:

        Return:
            A status code
        """

        self.debug_print("action_id", self.get_action_identifier())

        action_mapping = {
            "test_asset_connectivity": self._test_connectivity,
            "get_campaign_details": self._get_campaign_details,
            "get_campaign": self._get_campaign,
            "get_forensic_data": self._get_forensic_data,
            "get_forensic": self._get_forensic,
            "decode_url": self._decode_url,
            "on_poll": self._on_poll,
        }

        action = self.get_action_identifier()
        action_execution_status = phantom.APP_SUCCESS

        if action in list(action_mapping.keys()):
            action_function = action_mapping[action]
            action_execution_status = action_function(param)
        return action_execution_status


if __name__ == "__main__":
    import argparse

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)
    argparser.add_argument("-v", "--verify", action="store_true", help="verify", required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            print("Accessing the Login page")
            login_url = BaseConnector._get_phantom_base_url() + "login"
            r = requests.get(login_url, verify=verify)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platfrom. Error: " + str(e))
            sys.exit(1)

    if len(sys.argv) < 2:
        print("No test json specified as input")
        sys.exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = ProofpointConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
