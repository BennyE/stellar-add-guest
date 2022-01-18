#!/usr/bin/env python3

# This script is supposed to be executed directly and NOT via the event-action command!

# Written by Benjamin Eggerstedt in 2022
# Developed during my free time, thus not official ALE code.

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

#
# Imports
#
import sys
try:
    import requests
except ImportError as ie:
    print(ie)
    # python3 -m pip install requests
    sys.exit("Please install python-requests!")
import json
try:
    import urllib3
except ImportError as ie:
    print(ie)
    # This comes as dependency of requests, so should always be there.
    # python3 -m pip install urllib3
    sys.exit("Please install urllib3!")  
import time
import random
import string
# Not needed, thus saving some system resource
#import uuid
import datetime

#
# Functions
#

def send_mail(email_from, email_to, ssid_name, ga_username, ga_password, ga_valid_until, language,
                smtp_server, smtp_auth, smtp_user, smtp_port, smtp_password):

    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    #from email.MIMEMultipart import MIMEMultipart
    #from email.MIMEText import MIMEText
    #from email.MIMEImage import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    # Define these once; use them twice!
    strFrom = email_from
    strTo = email_to

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    if language == "de":
        msgRoot['Subject'] = "Neuer Gastzugang für Gäste-WLAN: {0}".format(ssid_name)
    else:
        msgRoot['Subject'] = "New guest account for guest SSID: {0}".format(ssid_name)
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # Generate an UUID for uniqe attachment Content-IDs
    # We don't need this for this module and will save some system resources
    content_id = "abcdefg"

    if language == "de":
        msgText = MIMEText("""
Hallo,
soeben wurde ein neuer Gastzugang für das WLAN \"{0}\" erstellt.
Benutzername: {1}
Passwort: {2}
Gültig bis: {3}
Bis bald!
        """.format(ssid_name, ga_username, ga_password, ga_valid_until))
    else:
        msgText = MIMEText("""
Hi,
a new guest account for SSID \"{0}\" was just created.
Username: {1}
Password: {2}
Valid until: {3}
Thanks,
Regards,
The ALE Stellar Wireless Team
        """.format(ssid_name, ga_username, ga_password, ga_valid_until))

    msgAlternative.attach(msgText)

    if language == "de":
        mail_content = """
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style>
body {{
background-color: #ebebeb;
width: 800px;
margin: 0 auto;
padding-top: 20px;
padding-bottom: 60px;
font-family: "HelveticaNeueLight", "HelveticaNeue-Light", "Helvetica Neue Light", "HelveticaNeue", "Helvetica Neue", 'TeXGyreHerosRegular', "Helvetica", "Tahoma", "Geneva", "Arial", sans-serif; font-weight:300; font-stretch:normal;
}}
a {{
color: #2e9ec9;
}}
h2 {{
font-family: Georgia;
font-weight: normal;
font-size: 80px;
margin-bottom: 20px;
}}
li b {{
font-weight: bold;
}}
h2 a {{
text-decoration: none;
color: #444444;
text-shadow: 1px 1px 0px white;
}}
h3 {{
font-family: Georgia;
font-size: 24px;
color: #444444;
text-shadow: 1px 1px 0px white;
}}
ul {{
margin-left: 0px;
margin-bottom: 40px;
padding-left: 0px;
}}
ul>li {{
font-size: 16px;
line-height: 1.4em;
list-style-type: none;
position: relative;
margin-bottom: 20px;
padding-left: 40px;
padding-top: 40px;
padding-right: 40px;
padding-bottom: 60px;
background: #fff;
color: #444444;
-webkit-box-shadow:0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
-moz-box-shadow:0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
box-shadow:0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
}}
li li {{
padding: 10px 10px 0px 5px;
font-size: 16px;
margin-bottom: 0px;
margin-left: 25px;
list-style-type: disc;
list-style-position: outside;
-webkit-box-shadow: none;
-moz-box-shadow: none;
box-shadow: none;
}}
ul>li:before, ul>li:after {{
content:"";
position:absolute;
z-index:-2;
}}
body > ul > li > a:first-child {{
position: absolute;
bottom: 30px;
right: 40px;
font-family: Georgia;
font-size: 12px;
}}
body > ul > li > a:first-child::before {{
font-size: 100%;
content: "Permalink: ";
}}
blockquote {{
font-family: Georgia;
font-style: italic;
padding-left: 10px;
margin-left: 20px;
}}
/* For Screens smaller than 800px width. Smaller margins on boxes and flexible widths */
@media only screen and (max-width: 800px){{
body {{
padding: 5px;
width: 93%;
margin: 0 auto;
}}
h2 {{
font-size: 50px;
margin-bottom: 20px;
}}
               
ul {{
margin-left: 0px;
margin-bottom: 20px;
padding-left: 0px;
}}
                          
ul>li {{
margin-bottom: 15px;
padding: 25px 25px 50px 25px;
}}
blockquote {{
padding-left: 0;
margin-left: 15px;
}}
}}
</style>
</head><body>
<p></p>
<ul>
<li>
<p><a href="https://www.al-enterprise.com/"><img src="cid:image1_{4}" height="60px"></a>
<a href="https://www.al-enterprise.com/"><img src="cid:image2_{4}" height="75px"></a>
</p>
<p>Hallo,</p>
<p>soeben wurde ein neuer Gastzugang für das WLAN \"{0}\" erstellt.</p>
<p>Benutzername: <b>{1}</b><br/>
Passwort: <b>{2}</b><br/>
Gültig bis: <b>{3}</b></p>
<p>
Danke und Gru&szlig;,<br>
Ihr ALE Stellar Wireless Team
</p>
</li>
</ul>
</body></html>
    """.format(ssid_name, ga_username, ga_password, ga_valid_until, content_id)
    else:
        mail_content = """
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style>
body {{
background-color: #ebebeb;
width: 800px;
margin: 0 auto;
padding-top: 20px;
padding-bottom: 60px;
font-family: "HelveticaNeueLight", "HelveticaNeue-Light", "Helvetica Neue Light", "HelveticaNeue", "Helvetica Neue", 'TeXGyreHerosRegular', "Helvetica", "Tahoma", "Geneva", "Arial", sans-serif; font-weight:300; font-stretch:normal;
}}
a {{
color: #2e9ec9;
}}
h2 {{
font-family: Georgia;
font-weight: normal;
font-size: 80px;
margin-bottom: 20px;
}}
li b {{
font-weight: bold;
}}
h2 a {{
text-decoration: none;
color: #444444;
text-shadow: 1px 1px 0px white;
}}
h3 {{
font-family: Georgia;
font-size: 24px;
color: #444444;
text-shadow: 1px 1px 0px white;
}}
ul {{
margin-left: 0px;
margin-bottom: 40px;
padding-left: 0px;
}}
ul>li {{
font-size: 16px;
line-height: 1.4em;
list-style-type: none;
position: relative;
margin-bottom: 20px;
padding-left: 40px;
padding-top: 40px;
padding-right: 40px;
padding-bottom: 60px;
background: #fff;
color: #444444;
-webkit-box-shadow:0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
-moz-box-shadow:0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
box-shadow:0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
}}
li li {{
padding: 10px 10px 0px 5px;
font-size: 16px;
margin-bottom: 0px;
margin-left: 25px;
list-style-type: disc;
list-style-position: outside;
-webkit-box-shadow: none;
-moz-box-shadow: none;
box-shadow: none;
}}
ul>li:before, ul>li:after {{
content:"";
position:absolute;
z-index:-2;
}}
body > ul > li > a:first-child {{
position: absolute;
bottom: 30px;
right: 40px;
font-family: Georgia;
font-size: 12px;
}}
body > ul > li > a:first-child::before {{
font-size: 100%;
content: "Permalink: ";
}}
blockquote {{
font-family: Georgia;
font-style: italic;
padding-left: 10px;
margin-left: 20px;
}}
/* For Screens smaller than 800px width. Smaller margins on boxes and flexible widths */
@media only screen and (max-width: 800px){{
body {{
padding: 5px;
width: 93%;
margin: 0 auto;
}}
h2 {{
font-size: 50px;
margin-bottom: 20px;
}}
               
ul {{
margin-left: 0px;
margin-bottom: 20px;
padding-left: 0px;
}}
                          
ul>li {{
margin-bottom: 15px;
padding: 25px 25px 50px 25px;
}}
blockquote {{
padding-left: 0;
margin-left: 15px;
}}
}}
</style>
</head><body>
<p></p>
<ul>
<li>
<p><a href="https://www.al-enterprise.com/"><img src="cid:image1_{4}" height="60px"></a>
<a href="https://www.al-enterprise.com/"><img src="cid:image2_{4}" height="75px"></a>
</p>
<p>Hi,</p>
<p>a new guest account for SSID \"{0}\" was just created.</p>
<p>Username: <b>{1}</b><br/>
Password: <b>{2}</b><br/>
Valid until: <b>{3}</b></p>
<p>
Thanks,
Regards,<br>
The ALE Stellar Wireless Team
</p>
</li>
</ul>
</body></html>
    """.format(ssid_name, ga_username, ga_password, ga_valid_until, content_id)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(mail_content, 'html')
    msgAlternative.attach(msgText)

    # ALE Logo
    fp = open('/flash/python/logos/al_enterprise_bk_50mm.png', 'rb')
#    fp = open('logos/al_enterprise_bk_50mm.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    # Avoid that the mail client can cache a previous QR code by giving a custom name
    msgImage.add_header('Content-ID', '<image1_{0}>'.format(content_id))
    msgRoot.attach(msgImage)

    # Stellar Logo
    fp = open('/flash/python/logos/stellar-logo.png', 'rb')
#    fp = open('logos/stellar-logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    # Avoid that the mail client can cache a previous QR code by giving a custom name
    msgImage.add_header('Content-ID', '<image2_{0}>'.format(content_id))
    msgRoot.attach(msgImage)

    # Send the email
    import smtplib
    # Fix for issue # 2 - Python3 SMTP ValueError: server_hostname cannot be an empty string or start with a leading dot 
    smtp = smtplib.SMTP(host=smtp_server, port=smtp_port)
    smtp.set_debuglevel(0)
    smtp.connect(host=smtp_server, port=smtp_port)

    if smtp_auth == "yes":
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        result = smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    else:
        result = smtp.sendmail(strFrom, strTo, msgRoot.as_string())

if __name__ == "__main__":
    # Load settings from settings.json file
    print("[+] Reading settings.json file")
    try:
# Depending on the target platform to run/host this script you may need to modify this
        with open("/flash/python/settings.json", "r") as json_data:
#        with open("settings.json", "r") as json_data:
            settings = json.load(json_data)
            ov_hostname = settings["ov_hostname"]
            ov_username = settings["ov_username"]
            ov_password = settings["ov_password"]
            validate_https_certificate = settings["validate_https_certificate"]
            email_from = settings["email_from"]
            send_emails = settings["send_emails"]
            ssid_name = settings["ssid_name"]
            smtp_server = settings["smtp_server"]
            smtp_auth = settings["smtp_auth"]
            smtp_user = settings["smtp_user"]
            smtp_port = settings["smtp_port"]
            smtp_password = settings["smtp_password"]
            language = settings["language"]
            # Note that email_to will override to sys.argv[2] if given
            email_to = settings["email_to"]
            guest_prefix = settings["guest_prefix"]
            guest_duration_in_days = settings["guest_duration_in_days"]
    except IOError as ioe:
        print(ioe)
        sys.exit("ERROR: Couldn't find/open settings.json file!")
    except TypeError as te:
        print(te)
        sys.exit("ERROR: Couldn't read json format!")

    # Validate that setting.json is configured and not using the default
    if ov_hostname == "omnivista.example.com":
        sys.exit("ERROR: Can't work with default template value for OmniVista hostname!")

    # Validate that the hostname is a hostname, not URL
    if "https://" in ov_hostname:
        print("[!] Found \"https://\" in ov_hostname, removing it!")
        ov_hostname = ov_hostname.lstrip("https://")

    # Validate that the hostname doesn't contain a "/"
    if "/" in ov_hostname:
        print("[!] Found \"/\" in hostname, removing it!")
        ov_hostname = ov_hostname.strip("/")

    # Figure out if HTTPS certificates should be validated
    # That should actually be the default, so we'll warn if disabled.

    if(validate_https_certificate.lower() == "yes"):
        check_certs = True
    else:
        # This is needed to get rid of a warning coming from urllib3 on self-signed certificates
        print("[!] Ignoring certificate warnings or self-signed certificates!")
        print("[!] You should really fix this!")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        check_certs = False    

    # We support to send the guest_account details via email to the account creator
    if len(sys.argv) == 2:
        print("[+] Updating email_to address to: {0}".format(sys.argv[1]))
        email_to = sys.argv[1]

    # Test connection to OmniVista
    print("[*] Attempting to connect to OmniVista server @ https://{0}".format(ov_hostname))

    req = requests.Session()

    # Use the ca-certificate store managed via Debian
    # This is just for development, should be commented out for production.
    #req.verify = "/etc/ssl/certs/"

    # Check if we die on the HTTPS certificate
    try:
        ov = req.get("https://{0}".format(ov_hostname), verify=check_certs)
    except requests.exceptions.SSLError as sslerror:
        print(sslerror)
        sys.exit("[!] Caught issues on certificate, try to change \"validate_https_certificate\" to \"no\" in settings.json. Exiting!")

    if ov.status_code == 200:
        print("[*] Connection to {0} successful!".format(ov_hostname))
    else:
        sys.exit("[!] Connection to {0} failed, exiting!".format(ov_hostname))

    ov_login_data = {"userName" : ov_username, "password" : ov_password}
    ov_header = {"Content-Type": "application/json"}

    # requests.post with json=payload was introduced in version 2.4.2
    # otherwise it would need to be "data=json.dumps(ov_login_data),"

    ov = req.post("https://{0}/rest-api/login".format(ov_hostname),
                headers=ov_header,
                json=ov_login_data,
                verify=check_certs)

    if ov.status_code == 200:
        token = ov.json()
        token = token["accessToken"]
        ov_header["Authorization"] = "Bearer {0}".format(token)
    else:
        sys.exit("[!] The connection to OmniVista was not successful! Exiting!")
    letters = string.ascii_lowercase
    # keep in mind that the minimum password length is 6!
    random_username = ''.join(random.choice(letters) for i in range(6))

    # Doesn't contain "l", "I", "O", "0" and "1" on purpose to avoid mistyping, thx Michael
    letters = "ABCDEFGHJKMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz"
    try:
        r = random.SystemRandom()
    except NotImplementedError as nie:
        print(nie)
        sys.exit("Your system doesn't provide a secure random generator!")

    # Generate a secure random password for Guest Accounts
    random_password = "".join(r.choice(letters) for _ in range(8))

    # Note that JAVA (on OV side in the backend) uses Milliseconds for epoch
    add_guest_data = {"creator":ov_username,
    "accountType":"Account",
    "description":"",
    "password":"{0}".format(random_password),
    "repeat":"{0}".format(random_password),
    "username":"{0}{1}".format(guest_prefix, random_username),
    "dataQuotaAmount":1000,
    "dateOfEffective":int(round(time.time() * 1000)),
    "accountValidityPeriod":int(round((time.time() + (86400 * guest_duration_in_days)) * 1000)),
    "dataQuota":"Disabled"}

    # Document who created the account
    if language == "de":
        add_guest_data["description"] = "Gastzugang wurde durch {0} erstellt".format(email_to) if len(sys.argv) == 2 else "Gastzugang wurde durch {0} erstellt".format(ov_username)
    else:
        add_guest_data["description"] = "Guest account was created by {0}".format(email_to) if len(sys.argv) == 2 else "Guest account was created by {0}".format(ov_username)

    # Create the guest account
    add_guest_resp = req.post("https://{0}/api/ham/guest/account/addAccount".format(ov_hostname), headers=ov_header, json=add_guest_data, verify=check_certs)

    if add_guest_resp.json()["errorCode"] != 0:
        sys.exit("Guest account creation failed with: {0}".format(add_guest_resp.json()["errorMessage"]))

    # Logout from API
    ov3 = req.get("https://{0}/rest-api/logout".format(ov_hostname), verify=check_certs)

    # Generate how long the Guest Account is valid
    if language == "de":
        ga_valid_until = datetime.datetime.fromtimestamp(add_guest_data["accountValidityPeriod"] / 1000).strftime('%d.%m.%Y %H:%M:%S')
    else:
        ga_valid_until = datetime.datetime.fromtimestamp(add_guest_data["accountValidityPeriod"] / 1000).strftime('%Y-%m-%d %H:%M:%S')

    if send_emails == "yes":
        send_mail(email_from, email_to, ssid_name, guest_prefix + random_username, random_password, ga_valid_until, language, smtp_server, smtp_auth, smtp_user, smtp_port, smtp_password)