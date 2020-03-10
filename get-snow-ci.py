#!/usr/bin/env python
# requires pysnow library
# pip install pysnow

"""get-snow-ci.py: Get SNOW CIs"""

# libraries
import pysnow, csv, configparser, requests, json
from colorama import Fore, Back, Style

__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Get SNOW CIs'
__credits__ = ['Rich Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

# read and parse config file
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

# create client object
s = pysnow.Client(instance=config['api_auth']['snow_instance'], user=config['api_auth']['api_user'], password=config['api_auth']['api_password'])

def decrypt_passwd(sid):
    print ('____Decrypting password for CI with sys_id: '+sid+'____')
    url = 'https://expertservicestest.service-now.com/api/fuss2/ci_password/'+sid+'/getcipassword'
#     print (url)
    payload  = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': config['api_auth']['api_key']
    }
    response = requests.request("GET", url, headers=headers, data = payload)
#     print(response.text.encode('utf8'))  
    json_data = response.text
    pwd_dict = json.loads(json_data)
#     Debug by echoing formated JSON string and pwd_dict
#     print(json.dumps(pwd_dict, indent = 4, sort_keys=True))
#     print(pwd_dict)
    decrypted_password = pwd_dict['result']['fs_password']
#     print (decrypted_password)
    return decrypted_password
    
def getcis():
    for (k, v) in config.items('tables'):
        print ('__Fetching '+k+' CIs from ServiceNow table: '+v+'__')
        # Get all CIs
        r = s.query(v, query={})
        # order by 'created_on' descending, then iterate over the result and print out number
        for record in r.get_multiple(order_by=['-created_on']):
              password = decrypt_passwd(record[config['fields']['sys_id']])
#               print(record[config['fields']['sys_id']])
#               print(record[config['fields']['ip']])
#               print(record[config['fields']['username']])
# #               print(record[config['fields']['password']])
#               print (password)
#               print(record[config['fields']['primary_access']])
#               print(record[config['fields']['secondary_access']])
              print ('______Logging CI with sys_id: '+record[config['fields']['sys_id']]+' to CSV file______')
              writer.writerow({'sys_id': record[config['fields']['sys_id']],
                               'ip': record[config['fields']['ip']],
                               'username': record[config['fields']['username']],
#                                'password': record[config['fields']['password']],
                               'password': password,
                               'primary_access': record[config['fields']['primary_access']],
                               'secondary_access': record[config['fields']['secondary_access']]
                              })
            
with open (config['local']['cmdb_data'], 'w') as outputfile:
    fieldnames = ['sys_id', 'ip', 'username', 'password', 'primary_access', 'secondary_access']
    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)   
    writer.writeheader()
    getcis()

 