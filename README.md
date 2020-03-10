# Validate SSH Logins

Access SNOW via API, iterate over CI items in SNOW CMDB and validate access using stored credentials

Install python requirements
```pip install -r requirements.txt```

validate-ssh-login.py:  Reads input file and validates each connection logging results to output
input and output files defined in config.ini

get-snow-ci.py:  Reads relevant ServiceNow data from a specific CMDB table

Working on:
- Add all relevant CMDB tables to the config.ini
- Add logic to get-snow-ci.py to read all relevant CI information from tables defined in the config.ini
- Parse JSON for required ServieNow fieds defiend below.
- Construct input file from parsed JSON
- Execute validate-ssh-login.py

Backlog:
- Open OpsGenie alert when a device login fails.
- Build Selenium test for HTTP/HTTPS login validation.
- Work on validating Windows host login, possibly using Remote PoSH for validation.

Requirements:
- All python requirements are in requirements.txt
- chromedriver
- libnss3-dev


Notes:

API call to get unencrypted password from ServiceNow
```https://expertservices.service-now.com/api/fuss2/ci_password/%7Bsys_id%7D/getcipassword```


ServiceNow Fields
```
sys_id
u_host_name
u_username
u_primary_acces_method
u_secondary_access_method
u_fs_password
```
### Access Methods
```
HTTP
HTTPS
Telnet
SSH	
Splashtop
VPN
RDP
VSphere
Application Client 
```

JSON Output
```
result : object : ip_address
result : object : u_secondary_access_method
```





