#!/usr/bin/python

#  Debug
## import os
## print "Content-type: text/html\n"
## import sys
## sys.stderr = sys.stdout

#  Copyright 2011 Jon Rifkin
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


# -----------------------------------------------------------------------
#  Usage
# -----------------------------------------------------------------------
#
#  Purpose
#      Authenticate users against a CAS server from your python cgi scripts.
#
#  Using in your script
#
#      import pycas
#      status, id, cookie = pycas.login(CAS_SERVER,THIS_SCRIPT)
#
#  Required Parameters
#
#      - CAS_SERVER : the url of your CAS server
#                     (for example, https://login.yoursite.edu).
#      - THIS_SCRIPT: the url of the calling python cgi script.
#
#  Returned Values
#
#      - status:  return code, 0 for success.
#      - id    :  the user name returned by cas.
#      - cookie:  when non-blank, send this cookie to the client's
#                 browser so it can authenticate for the rest of the
#                 session.
#
#  Optional Parmaters:
#      - lifetime:  lifetime of the cookie in seconds, enforced by pycas.
#                   Default is 0, meaning unlimited lifetime.
#      - path:      Authentication cookie applies for all urls under 'path'.
#                   Defaults to "/" (all urls).
#      - protocol:  CAS protocol version.  Default is 2.  Can be set to 1.
#      - secure:    Default is 1, which authenticates for https connections only.
#      - opt:       set to 'renew' or 'gateway' for these CAS options.
#
#        Examples:
#          status, id, cookie = pycas.login(CAS_SERVER,THIS_SCRIPT,protocol=1,secure=0)
#          status, id, cookie = pycas.login(CAS_SERVER,THIS_SCRIPT,path="/cgi-bin/accts")
#
#   Status Codes are listed below.
#

# -----------------------------------------------------------------------
#  Constants
# -----------------------------------------------------------------------
#
#  Secret used to produce hash.   This can be any string.  Hackers
#  who know this string can forge this script's authentication cookie.
SECRET = "7e16162998eb7efafb1498f75190a937"

#  Name field for pycas cookie
PYCAS_NAME = "pycas"

#  CAS Staus Codes:  returned to calling program by login() function.
CAS_OK = 0  # CAS authentication successful.
CAS_COOKIE_EXPIRED = 1  # PYCAS cookie exceeded its lifetime.
CAS_COOKIE_INVALID = 2  # PYCAS cookie is invalid (probably corrupted).
CAS_TICKET_INVALID = 3  # CAS server ticket invalid.
CAS_GATEWAY = 4  # CAS server returned without ticket while in gateway mode.

#  Status codes returned internally by function get_cookie_status().
COOKIE_AUTH = 0  # PYCAS cookie is valid.
COOKIE_NONE = 1  # No PYCAS cookie found.
COOKIE_GATEWAY = 2  # PYCAS gateway cookie found.
COOKIE_INVALID = 3  # Invalid PYCAS cookie found.

#  Status codes returned internally by function get_ticket_status().
TICKET_OK = 0  # Valid CAS server ticket found.
TICKET_NONE = 1  # No CAS server ticket found.
TICKET_INVALID = 2  # Invalid CAS server ticket found.

CAS_MSG = (
    "CAS authentication successful.",
    "PYCAS cookie exceeded its lifetime.",
    "PYCAS cookie is invalid (probably corrupted).",
    "CAS server ticket invalid.",
    "CAS server returned without ticket while in gateway mode.",
)

# ##Optional log file for debugging
# ##LOG_FILE="/tmp/cas.log"


# -----------------------------------------------------------------------
#  Imports
# -----------------------------------------------------------------------
import os
import cgi
import md5
import time
import urllib
import urlparse


# -----------------------------------------------------------------------
#  Functions
# -----------------------------------------------------------------------

#  For debugging.
def writelog(msg):
    f = open(LOG_FILE, "a")
    timestr = time.strftime("%Y-%m-%d %H:%M:%S ");
    f.write(timestr + msg + "\n");
    f.close()


#  Used for parsing xml.  Search str for first occurance of
#  <tag>.....</tag> and return text (striped of leading and
#  trailing whitespace) between tags.  Return "" if tag not
#  found.
def parse_tag(str, tag):
    tag1_pos1 = str.find("<" + tag)
    #  No tag found, return empty string.
    if tag1_pos1 == -1: return ""
    tag1_pos2 = str.find(">", tag1_pos1)
    if tag1_pos2 == -1: return ""
    tag2_pos1 = str.find("</" + tag, tag1_pos2)
    if tag2_pos1 == -1: return ""
    return str[tag1_pos2 + 1:tag2_pos1].strip()


#  Split string in exactly two pieces, return '' for missing pieces.
def split2(str, sep):
    parts = str.split(sep, 1) + ["", ""]
    return parts[0], parts[1]


#  Use hash and secret to encrypt string.
def makehash(str, secret=SECRET):
    m = md5.new()
    m.update(str)
    m.update(SECRET)
    return m.hexdigest()[0:8]


#  Form cookie
def make_pycas_cookie(val, domain, path, secure, expires=None):
    cookie = "Set-Cookie: %s=%s;domain=%s;path=%s" % (PYCAS_NAME, val, domain, path)
    if secure:
        cookie += ";secure"
    if expires:
        cookie += ";expires=" + expires
    return cookie


#  Send redirect to client.  This function does not return, i.e. it teminates this script.
def do_redirect(cas_host, service_url, opt, secure):
    cas_url = cas_host + "/cas/login?service=" + service_url
    if opt in ("renew", "gateway"):
        cas_url += "&%s=true" % opt
    # Print redirect page to browser
    print
    "Refresh: 0; url=%s" % cas_url
    print
    "Content-type: text/html"
    if opt == "gateway":
        domain, path = urlparse.urlparse(service_url)[1:3]
        print
        make_pycas_cookie("gateway", domain, path, secure)
    print
    """
If your browser does not redirect you, then please follow <a href="%s">this link</a>.
""" % (cas_url)
    raise SystemExit


#  Retrieve id from pycas cookie and test data for validity
# (to prevent mailicious users from falsely authenticating).
#  Return status and id (id will be empty string if unknown).
def decode_cookie(cookie_vals, lifetime=None):
    #  Test for now cookies
    if cookie_vals == None:
        return COOKIE_NONE, ""

    # Test each cookie value
    cookie_attrs = []
    for cookie_val in cookie_vals:
        #  Remove trailing ;
        if cookie_val and cookie_val[-1] == ";":
            cookie_val = cookie_val[0:-1]

        # Test for pycas gateway cookie
        if cookie_val == "gateway":
            cookie_attrs.append(COOKIE_GATEWAY)

        # Test for valid pycas authentication cookie.
        else:
            # Separate cookie parts
            oldhash = cookie_val[0:8]
            timestr, id = split2(cookie_val[8:], ":")
            #  Verify hash
            newhash = makehash(timestr + ":" + id)
            if oldhash == makehash(timestr + ":" + id):
                #  Check lifetime
                if lifetime:
                    if str(int(time.time() + int(lifetime))) < timestr:
                        #  OK:  Cookie still valid.
                        cookie_attrs.append(COOKIE_AUTH)
                    else:
                        # ERROR:  Cookie exceeded lifetime
                        cookie_attrs.append(COOKIE_EXPIRED)
                else:
                    #  OK:  Cookie valid (it has no lifetime)
                    cookie_attrs.append(COOKIE_AUTH)

            else:
                #  ERROR:  Cookie value are not consistent
                cookie_attrs.append(COOKIE_INVALID)

    # Return status according to attribute values

    #  Valid authentication cookie takes precedence
    if COOKIE_AUTH in cookie_attrs:
        return COOKIE_AUTH, id
    # Gateway cookie takes next precedence
    if COOKIE_GATEWAY in cookie_attrs:
        return COOKIE_GATEWAY, ""
    # If we've gotten here, there should be only one attribute left.
    return cookie_attrs[0], ""


#  Validate ticket using cas 1.0 protocol
def validate_cas_1(cas_host, service_url, ticket):
    #  Second Call to CAS server: Ticket found, verify it.
    cas_validate = cas_host + "/cas/validate?ticket=" + ticket + "&service=" + service_url
    f_validate = urllib.urlopen(cas_validate)
    #  Get first line - should be yes or no
    response = f_validate.readline()
    #  Ticket does not validate, return error
    if response == "no\n":
        f_validate.close()
        return TICKET_INVALID, ""
    # Ticket validates
    else:
        #  Get id
        id = f_validate.readline()
        f_validate.close()
        id = id.strip()
        return TICKET_OK, id


# Validate ticket using cas 2.0 protocol
#    The 2.0 protocol allows the use of the mutually exclusive "renew" and "gateway" options.
def validate_cas_2(cas_host, service_url, ticket, opt):
    #  Second Call to CAS server: Ticket found, verify it.
    cas_validate = cas_host + "/cas/serviceValidate?ticket=" + ticket + "&service=" + service_url
    if opt:
        cas_validate += "&%s=true" % opt
    f_validate = urllib.urlopen(cas_validate)
    #  Get first line - should be yes or no
    response = f_validate.read()
    id = parse_tag(response, "cas:user")
    #  Ticket does not validate, return error
    if id == "":
        return TICKET_INVALID, ""
    # Ticket validates
    else:
        return TICKET_OK, id


# Read cookies from env variable HTTP_COOKIE.
def get_cookies():
    #  Read all cookie pairs
    try:
        cookie_pairs = os.getenv("HTTP_COOKIE").split()
    except AttributeError:
        cookie_pairs = []
    cookies = {}
    for cookie_pair in cookie_pairs:
        key, val = split2(cookie_pair.strip(), "=")
        if cookies.has_key(key):
            cookies[key].append(val)
        else:
            cookies[key] = [val, ]
    return cookies


#  Check pycas cookie
def get_cookie_status():
    cookies = get_cookies()
    return decode_cookie(cookies.get(PYCAS_NAME))


def get_ticket_status(cas_host, service_url, protocol, opt):
    if cgi.FieldStorage().has_key("ticket"):
        ticket = cgi.FieldStorage()["ticket"].value
        if protocol == 1:
            ticket_status, id = validate_cas_1(cas_host, service_url, ticket, opt)
        else:
            ticket_status, id = validate_cas_2(cas_host, service_url, ticket, opt)
        # Make cookie and return id
        if ticket_status == TICKET_OK:
            return TICKET_OK, id
        # Return error status
        else:
            return ticket_status, ""
    else:
        return TICKET_NONE, ""


# -----------------------------------------------------------------------
#  Exported functions
# -----------------------------------------------------------------------

#  Login to cas and return user id.
#
#   Returns status, id, pycas_cookie.
#
def login(cas_host, service_url, lifetime=None, secure=1, protocol=2, path="/", opt=""):
    #  Check cookie for previous pycas state, with is either
    #     COOKIE_AUTH    - client already authenticated by pycas.
    #     COOKIE_GATEWAY - client returning from CAS_SERVER with gateway option set.
    #  Other cookie status are
    #     COOKIE_NONE    - no cookie found.
    #     COOKIE_INVALID - invalid cookie found.
    cookie_status, id = get_cookie_status()

    if cookie_status == COOKIE_AUTH:
        return CAS_OK, id, ""

    if cookie_status == COOKIE_INVALID:
        return CAS_COOKIE_INVALID, "", ""

    # Check ticket ticket returned by CAS server, ticket status can be
    #     TICKET_OK      - a valid authentication ticket from CAS server
    #     TICKET_INVALID - an invalid authentication ticket.
    #     TICKET_NONE    - no ticket found.
    #  If ticket is ok, then user has authenticated, return id and
    #  a pycas cookie for calling program to send to web browser.
    ticket_status, id = get_ticket_status(cas_host, service_url, protocol, opt)

    if ticket_status == TICKET_OK:
        timestr = str(int(time.time()))
        hash = makehash(timestr + ":" + id)
        cookie_val = hash + timestr + ":" + id
        domain = urlparse.urlparse(service_url)[1]
        return CAS_OK, id, make_pycas_cookie(cookie_val, domain, path, secure)

    elif ticket_status == TICKET_INVALID:
        return CAS_TICKET_INVALID, "", ""

    # If unathenticated and in gateway mode, return gateway status and clear
    #  pycas cookie (which was set to gateway by do_redirect()).
    if opt == "gateway":
        if cookie_status == COOKIE_GATEWAY:
            domain, path = urlparse.urlparse(service_url)[1:3]
            #  Set cookie expiration in the past to clear the cookie.
            past_date = time.strftime("%a, %d-%b-%Y %H:%M:%S %Z", time.localtime(time.time() - 48 * 60 * 60))
            return CAS_GATEWAY, "", make_pycas_cookie("", domain, path, secure, past_date)

    # Do redirect
    do_redirect(cas_host, service_url, opt, secure)


# -----------------------------------------------------------------------
#  Test
# -----------------------------------------------------------------------


if __name__ == "__main__":

    CAS_SERVER = "https://login.uconn.edu"
    SERVICE_URL = "http://bluet.ucc.uconn.edu/~jon/cgi-bin/pycas.py"

    status, id, cookie = login(CAS_SERVER, SERVICE_URL, secure=0, opt="gateway")

    print
    "Content-type: text/html"
    print
    cookie
    print
    print
    """
<html>
<head>
<title>
castest.py
</title>
<style type=text/css>
td {background-color: #dddddd; padding: 4px}
</style>
</head>
<body>
<h2>pycas.py</h2>
<hr>
"""
    #  Print browser parameters from pycas.login
    if cgi.FieldStorage().has_key("ticket"):
        ticket = cgi.FieldStorage()["ticket"].value
    else:
        ticket = ""

    in_cookie = os.getenv("HTTP_COOKIE")

    print
    """
<p>
<b>Parameters sent from browser</b>
<table>
<tr> <td>Ticket</td> <td>%s</td> </tr> 
<tr> <td>Cookie</td> <td>%s</td> </tr> 
</table>
</p>""" % (ticket, in_cookie)

    #  Print output from pycas.login
    print
    """
<p>
<b>Parameters returned from pycas.login()</b>
<table>
<tr><td>status</td><td> <b>%s</b> - <i>%s</i></td></tr>
<tr><td>id</td><td> <b>%s</b></td></tr>
<tr><td>cookie</td><td> <b>%s</b></td></tr>
</table>
</p>
</body></html>""" % (status, CAS_MSG[status], id, cookie)