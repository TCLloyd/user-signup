#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
#
import webapp2
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)
def valid_password(password):
    return ((len(password) >= 3) and (len(password) <= 20))

def valid_verify(verify, password):
    return (verify == password)

def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)

username_error = ""
password_error = ""
verify_error = ""
email_error = ""
username = ""
email = ""

signup_form = """
<h2>Signup</h2>
<form method="post">
<table>
    <tr>
        <td>
            <label for="username">
                Username
                <input type="text" name="username" value="{4}" required>
            </label>
        </td>
        <td>
            <span class="error" style="color:red">{0}</span>
        </td>
    </tr>
    <tr>
        <td>
            <label for="password">
                Password
                <input type="password" name="password" required>
            </label>
        </td>
        <td>
            <span class="error" style="color:red">{1}</span>
        </td>
    </tr>
    <tr>
        <td>
            <label for="verify">
                Verify Password
                <input type="password" name="verify" required>
            </label>
        </td>
        <td>
            <span class="error" style="color:red">{2}</span>
        </td>
    </tr>
    <tr>
        <td>
            <label for="email">
                Email (optional)
                <input type="email" name="email" value="{5}">
            </label>
        </td>
        <td>
            <span class="error" style="color:red">{3}</span>
        </td>
    </tr>
</table>
<input type="submit">
</form>
"""

class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error, password_error, verify_error, email_error, username, email):
        content = page_header + signup_form + page_footer
        self.response.write(content.format(username_error, password_error, verify_error,
        email_error, username, email))

    def get(self):
        self.write_form(username_error="", password_error="",
         verify_error="", email_error="", username="", email="")

    def post(self):
            have_error = False
            username = self.request.get("username")
            password = self.request.get("password")
            verify = self.request.get("verify")
            email = self.request.get("email")

            if not valid_username(username):
                have_error = True
                username_error = "This is not a valid username."
            else:
                username_error = ""
            if not valid_password(password):
                have_error = True
                password_error = "This is not a valid password."
            else:
                password_error = ""
            if not valid_verify(verify, password):
                have_error = True
                verify_error = "Passwords do not match."
            else:
                verify_error = ""
            if not valid_email(email):
                have_error = True
                email_error = "This is not a valid email."
            else:
                email_error = ""
            if have_error == True:
                self.write_form(username_error, password_error, verify_error, email_error, username, email)
            else:
                self.redirect('/Welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        welcome_message = "<h3>Welcome " + username + "!</h3>"
        content = page_header + welcome_message + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', Welcome)
], debug=True)
