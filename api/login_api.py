# -*- coding: utf-8 -*-
# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from google.oauth2 import id_token
from google.auth.transport import requests

from framework import basehandlers
from framework import users
import settings


class LoginAPI(basehandlers.APIHandler):
  """Create a session using the credential generated by Sign-In With Google."""

  def do_post(self, **kwargs):
    # TODO(jrobbins): Remove id_token after next deployment.
    token = (self.get_param('id_token', required=False) or
             self.get_param('credential'))
    message = "Unable to Authenticate. Please sign in again."

    try:
      idinfo = id_token.verify_oauth2_token(
          token, requests.Request(),
          settings.GOOGLE_SIGN_IN_CLIENT_ID)
      users.add_signed_user_info_to_session(idinfo['email'])
      self._update_last_visit_field(idinfo['email'])
      message = "Done"
      # print(idinfo['email'], file=sys.stderr)
    except ValueError:
      message = "Invalid token"

    return {'message': message}
