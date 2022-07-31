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
import uuid
import datetime
try:
    import pyqrcode
except ImportError as ie:
    sys.exit("Please install pyqrcode & pypng!")

#
# Functions
#

def add_qr_code(language, content_id, print_cleartext_psk, psk):
    if language == "de":
        qr_text = f"""
        <p>
        Scannen Sie den folgenden QR-Code um Zugriff auf das Wireless LAN zu erhalten:</br>
        <center><img src="cid:image3_{content_id}" style="max-height: 150px;"></img>
        {'</br>Pre-Shared Key (PSK): ' + psk if print_cleartext_psk == "yes" else ""}</center>
        </p>
        """
    else:
        qr_text = f"""
        <p>
        Scan the following QR code to get access to the Wi-Fi network:</br>
        <center><img src="cid:image3_{content_id}" style="max-height: 150px;"></img>
        {'</br>Pre-Shared Key (PSK): ' + psk if print_cleartext_psk == "yes" else ""}</center>
        </p>
        """
    return qr_text

def send_mail(email_from, email_to, ssid_name, ga_username, ga_password, ga_valid_until, language,
                smtp_server, smtp_auth, smtp_user, smtp_port, smtp_password, send_psk_via_mail, psk, print_cleartext_psk):

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
        msgRoot['Subject'] = f"Neuer Gastzugang für Gäste-WLAN: {ssid_name}"
    else:
        msgRoot['Subject'] = f"New guest account for guest SSID: {ssid_name}"
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # Generate an UUID for uniqe attachment Content-IDs
    # Re-introduced for QR code functionality
    content_id = uuid.uuid1().hex

    if language == "de":
        msgText = MIMEText(f"""
Hallo,
soeben wurde ein neuer Gastzugang für das WLAN \"{ssid_name}\" erstellt.
Benutzername: {ga_username}
Passwort: {ga_password}
Gültig bis: {ga_valid_until}
{'Pre-Shared Key (PSK): ' + psk if print_cleartext_psk == "yes" else ""}
Bis bald!
        """)
    else:
        msgText = MIMEText(f"""
Hi,
a new guest account for SSID \"{ssid_name}\" was just created.
Username: {ga_username}
Password: {ga_password}
Valid until: {ga_valid_until}
{'Pre-Shared Key (PSK): ' + psk if print_cleartext_psk == "yes" else ""}
Thanks,
Regards,
The ALE Stellar Wireless Team
        """)

    msgAlternative.attach(msgText)

    if language == "de":
        mail_content = f"""
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
<table>
<tr>
<td>
<a href="https://www.al-enterprise.com/"><img src="cid:image1_{content_id}" style="max-height: 60px;"></img></a>
</td>
<td>&nbsp;</td>
<td>
<a href="https://www.al-enterprise.com/"><img src="cid:image2_{content_id}" style="max-height: 75px;"></img></a>
</td>
</tr>
</table>
<p>Hallo,</p>
<p>soeben wurde ein neuer Gastzugang für das WLAN \"{ssid_name}\" erstellt.</p>
<p>Benutzername: <b>{ga_username}</b><br/>
Passwort: <b>{ga_password}</b><br/>
Gültig bis: <b>{ga_valid_until}</b></p>
{add_qr_code(language, content_id, print_cleartext_psk, psk) if send_psk_via_mail == "yes" else ""}
<p>
Danke und Gru&szlig;,<br>
Ihr ALE Stellar Wireless Team
</p>
</li>
</ul>
</body></html>
    """
    else:
        mail_content = f"""
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
<table>
<tr>
<td>
<a href="https://www.al-enterprise.com/"><img src="cid:image1_{content_id}" style="max-height: 60px;"></img></a>
</td>
<td>&nbsp;</td>
<td>
<a href="https://www.al-enterprise.com/"><img src="cid:image2_{content_id}" style="max-height: 75px;"></img></a>
</td>
</tr>
</table>
<p>Hi,</p>
<p>a new guest account for SSID \"{ssid_name}\" was just created.</p>
<p>Username: <b>{ga_username}</b><br/>
Password: <b>{ga_password}</b><br/>
Valid until: <b>{ga_valid_until}</b></p>
{add_qr_code(language, content_id, print_cleartext_psk, psk) if send_psk_via_mail == "yes" else ""}
<p>
Thanks,
Regards,<br>
The ALE Stellar Wireless Team
</p>
</li>
</ul>
</body></html>
    """

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(mail_content, 'html')
    msgAlternative.attach(msgText)

    # ALE Logo
    if runs_on_omniswitch == "yes":
        fp = open('/flash/python/logos/al_enterprise_bk_50mm.png', 'rb')
    else:
        fp = open('logos/al_enterprise_bk_50mm.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    # Avoid that the mail client can cache a previous QR code by giving a custom name
    msgImage.add_header('Content-ID', f'<image1_{content_id}>')
    msgRoot.attach(msgImage)

    # Stellar Logo
    if runs_on_omniswitch == "yes":
        fp = open('/flash/python/logos/stellar-logo.png', 'rb')
    else:
        fp = open('logos/stellar-logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    # Avoid that the mail client can cache a previous QR code by giving a custom name
    msgImage.add_header('Content-ID', f'<image2_{content_id}>')
    msgRoot.attach(msgImage)

    # Add QR Code
    if send_psk_via_mail == "yes":
        # Generate a QR code to login to this SSID
        # QR format: "WIFI:T:WPA;S:SSID;P:PSK;;"
        if encryption != "OPEN":
            pskqr = pyqrcode.create(f"WIFI:T:{encryption};S:{ssid_name};P:{psk};;")
        else:
            pskqr = pyqrcode.create(f"WIFI:T:nopass;S:{ssid_name};P:;;")
        if runs_on_omniswitch == "yes":
            pskqr.png("/flash/python/logos/qrcode.png", scale=8)
            fp = open('/flash/python/logos/qrcode.png', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
        else:
            pskqr.png("logos/qrcode.png", scale=8)
            fp = open('logos/qrcode.png', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
        msgImage.add_header('Content-ID', f'<image3_{content_id}>')
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
#        with open("/flash/python/settings.json", "r") as json_data:
        with open("settings.json", "r") as json_data:
            settings = json.load(json_data)
            ov_hostname = settings["ov_hostname"]
            ov_username = settings["ov_username"]
            ov_password = settings["ov_password"]
            validate_https_certificate = settings["validate_https_certificate"]
            email_from = settings["email_from"]
            send_emails = settings["send_emails"]
            ssid_name = settings["ssid_name"]
            encryption = settings["encryption"]
            psk = settings["psk"]
            print_cleartext_psk = settings["print_cleartext_psk"]
            send_psk_via_mail = settings["send_psk_via_mail"]
            runs_on_omniswitch = settings["runs_on_omniswitch"]
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
        print(f"[+] Updating email_to address to: {sys.argv[1]}")
        email_to = sys.argv[1]

    # Test connection to OmniVista
    print(f"[*] Attempting to connect to OmniVista server @ https://{ov_hostname}")

    req = requests.Session()

    # Use the ca-certificate store managed via Debian
    # This is just for development, should be commented out for production.
    #req.verify = "/etc/ssl/certs/"

    # Check if we die on the HTTPS certificate
    try:
        ov = req.get(f"https://{ov_hostname}", verify=check_certs)
    except requests.exceptions.SSLError as sslerror:
        print(sslerror)
        sys.exit("[!] Caught issues on certificate, try to change \"validate_https_certificate\" to \"no\" in settings.json. Exiting!")

    if ov.status_code == 200:
        print(f"[*] Connection to {ov_hostname} successful!")
    else:
        sys.exit(f"[!] Connection to {ov_hostname} failed, exiting!")

    ov_login_data = {"userName" : ov_username, "password" : ov_password}
    ov_header = {"Content-Type": "application/json"}

    # requests.post with json=payload was introduced in version 2.4.2
    # otherwise it would need to be "data=json.dumps(ov_login_data),"

    ov = req.post(f"https://{ov_hostname}/rest-api/login",
                headers=ov_header,
                json=ov_login_data,
                verify=check_certs)

    if ov.status_code == 200:
        ov_header["Authorization"] = f"Bearer {ov.json()['accessToken']}"
    else:
        sys.exit("[!] The connection to OmniVista was not successful! Exiting!")
    letters = string.ascii_lowercase
    random_username = ''.join(random.choice(letters) for _ in range(6))

    # You may need to adapt this to your local language
    undesireable_words = ["cunt", "pussy", "nigger", "penis", "fotze", "hitler", "fuck"]

    for uw in undesireable_words:
        if uw in random_username:
            print("[!] Detected undesirable word in username, generating a new one!")
            # I assume our chances are very low to generate two undesireable words in a row
            random_username = ''.join(random.choice(letters) for _ in range(6))
            break

    # Doesn't contain "l", "I", "O", "0" and "1" on purpose to avoid mistyping, thx Michael
    letters = "ABCDEFGHJKMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz"
    try:
        r = random.SystemRandom()
    except NotImplementedError as nie:
        print(nie)
        sys.exit("Your system doesn't provide a secure random generator!")

    # Generate a secure random password for Guest Accounts
    random_password = "".join(r.choice(letters) for _ in range(8))

    for uw in undesireable_words:
        if uw in random_password.lower():
            print("[!] Detected undesirable word in password, generating a new one!")
            # I assume our chances are very low to generate two undesireable words in a row
            random_password = "".join(r.choice(letters) for _ in range(8))
            break

    # Note that JAVA (on OV side in the backend) uses Milliseconds for epoch
    add_guest_data = {"creator":ov_username,
    "accountType":"Account",
    "description":"",
    "password":f"{random_password}",
    "repeat":f"{random_password}",
    "username":f"{guest_prefix}{random_username}",
    "dataQuotaAmount":1000,
    "dateOfEffective":int(round(time.time() * 1000)),
    "accountValidityPeriod":int(round((time.time() + (86400 * guest_duration_in_days)) * 1000)),
    "dataQuota":"Disabled"}

    # Document who created the account
    if language == "de":
        add_guest_data["description"] = f"Gastzugang wurde durch {email_to} erstellt" if len(sys.argv) == 2 else f"Gastzugang wurde durch {ov_username} erstellt"
    else:
        add_guest_data["description"] = f"Guest account was created by {email_to}" if len(sys.argv) == 2 else f"Guest account was created by {ov_username}"

    # Create the guest account
    add_guest_resp = req.post(f"https://{ov_hostname}/api/ham/guest/account/addAccount", headers=ov_header, json=add_guest_data, verify=check_certs)

    if add_guest_resp.json()["errorCode"] != 0:
        sys.exit(f"Guest account creation failed with: {add_guest_resp.json()['errorMessage']}")

    # Logout from API
    ov3 = req.get(f"https://{ov_hostname}/rest-api/logout", verify=check_certs)

    # Generate how long the Guest Account is valid
    if language == "de":
        ga_valid_until = datetime.datetime.fromtimestamp(add_guest_data["accountValidityPeriod"] / 1000).strftime('%d.%m.%Y %H:%M:%S')
    else:
        ga_valid_until = datetime.datetime.fromtimestamp(add_guest_data["accountValidityPeriod"] / 1000).strftime('%Y-%m-%d %H:%M:%S')

    if send_emails == "yes":
        send_mail(email_from, email_to, ssid_name, guest_prefix + random_username, random_password, ga_valid_until, language, smtp_server,
                    smtp_auth, smtp_user, smtp_port, smtp_password, send_psk_via_mail, psk, print_cleartext_psk)