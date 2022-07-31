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
![image](https://user-images.githubusercontent.com/5174414/150029499-7d9003d2-8e34-4867-880e-d698b7adffb0.png)

## Language set to German (settings.json -> "language": "de") 
![image](https://user-images.githubusercontent.com/5174414/150029836-2f4997ac-7808-4c60-9de1-73c1fa7c6931.png)

## New functions in this branch/release

