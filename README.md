# stellar-add-guest
stellar-add-guest is a small tool to generate a new guest for Stellar Wireless (Enterprise mode) in OmniVista 2500 hosted on OmniSwitch with AOS Release 8.

## Overview (meant to be executed on OmniSwitch with access to OmniVista 2500)
![image](https://user-images.githubusercontent.com/5174414/150031492-3dbfc95d-4b2c-4882-a074-0547b2645a79.png)

## Edit the settings-example.json and store it as settings.json
```
{
    "ov_hostname": "hostname or IP address of OV e.g. omnivista.home but without https",
    "ov_username": "admin",
    "ov_password": "<your ov admin password>",
    "validate_https_certificate": "no",
    "send_emails": "yes",
    "ssid_name": "Stellar-Captive",
    "encryption": "WPA/WPA2 or OPEN",
    "psk": "The PSK of the SSID, ignored if encryption is set to OPEN",
    "print_cleartext_psk": "yes",
    "send_psk_via_mail": "yes",
    "runs_on_omniswitch": "yes",
    "email_from": "<your from email address>",
    "smtp_server": "smtp.gmail.com",
    "smtp_auth": "yes",
    "smtp_port": 587,
    "smtp_user": "<your SMTP login name, often your email_from>",
    "smtp_password": "<your SMTP password>",
    "language": "de",
    "email_to": "<your email_to, if no argv is given>",
    "guest_prefix": "gast_",
    "guest_duration_in_days": 31
}
```
## Execute the Python script on the OmniSwitch
```
Router-> python3 /flash/python/stellar-add-guest.py <email-address@mailaddressdomain.com>
[+] Reading settings.json file
[!] Ignoring certificate warnings or self-signed certificates!
[!] You should really fix this!
[+] Updating email_to address to: <email-address@mailaddressdomain.com>
[*] Attempting to connect to OmniVista server @ https://omnivista.home
[*] Connection to omnivista.home successful!
````
## Language set to English (settings.json -> "language": "en") 
- language = "en"
- send_psk_via_mail = "yes"
- print_cleartext_psk" = "yes"
![Screenshot 2022-07-31 at 21 30 00](https://user-images.githubusercontent.com/5174414/182043022-911f68d2-d47b-4250-8219-33acd8f5ba22.png)

## Language set to German (settings.json -> "language": "de") 
- language = "de"
- send_psk_via_mail = "yes"
- print_cleartext_psk" = "no"
![Screenshot 2022-07-31 at 21 11 07](https://user-images.githubusercontent.com/5174414/182043031-9bef3ec7-9df2-4404-8b73-5e19b2ee87fa.png)

## New functions in this branch/release
- Adds QR Code feature request (Issue https://github.com/BennyE/stellar-add-guest/issues/1)
 - Set "send_psk_via_mail" to "no" if you don't want a QR Code 
- Adds "runs_on_omniswitch" setting, to comment/uncomment less lines depending on OmniSwitch (AOS R8) or standard environment
- Adds simple check against undesireable words in random guest username / password (you may want to modify this)
- Modified all .format() to more modern Python f-Strings
- HTML mail looks slightly better in Apple Mail now
