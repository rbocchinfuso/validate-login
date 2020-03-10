#!/usr/bin/env python

"""validate-ssh-login.py: Validate SSH Login"""

# libraries
import paramiko, time, csv, json, jsonify, configparser
from colorama import Fore, Back, Style

__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Validate SSH Login'
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

def check_ssh(ip, user, password, initial_wait=0, interval=0, retries=1):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    time.sleep(initial_wait)

    for x in range(retries):
        try:
            client.connect(ip, username=user, password=password)
            print (Fore.WHITE + Back.GREEN + '___TEST RESULT: '+ip + ',' + user + ',' + 'success___'+ Style.RESET_ALL)
            writer.writerow({'host': ip, 'user': user, 'status': 'success'})
            return True
        except Exception as e:
            print (Fore.RED + Back.YELLOW + ip + ',' + user + ',' + str(e) + Style.RESET_ALL)
            writer.writerow({'host': ip, 'user': user, 'status': str(e)})
            time.sleep(interval)
    return False

def validate_cmdb_data(sys_id, ip, user, password, primary_access, secondary_access):
    if (primary_access != 'SSH' and secondary_access != 'SSH'):
        print (Fore.RED + Back.YELLOW + '______SSH not defined as a valid primary or secondary access method for CI sys_id: '+sys_id+' with IP address: '+ip+'______'+ Style.RESET_ALL)
        return;
    if (primary_access == 'SSH'):
        print (Fore.CYAN + '______Testing SSH login for CI sys_id '+sys_id+' with IP address: '+ip+'______' + Style.RESET_ALL)
        check_ssh (ip, user, password)
    if (secondary_access == 'SSH'):
        print (Fore.CYAN + '______Testing SSH login for CI sys_id '+sys_id+' with IP address: '+ip+'______' + Style.RESET_ALL)
        check_ssh (ip, user, password)
            
inputfile = config['local']['cmdb_data']
with open(inputfile) as inputfile:
    csvreader = csv.reader(inputfile, delimiter=',')
    next(csvreader)
    with open (config['local']['validation_data'], 'w') as outputfile:
        fieldnames = ['host', 'user', 'status']
        writer = csv.DictWriter(outputfile, fieldnames=fieldnames)   
        writer.writeheader()
        for row in csvreader:
            print('__Validating CI with sys_id: ' + row[0] + 'and IP: '+ row[1] + '__')
            if (len(row[3]) != 0):
                print (Fore.CYAN + '____CI item with sys_id: '+row[0]+' has a valid password, continuing validation process for CI with IP address: '+row[1]+'____' + Style.RESET_ALL)
                validate_cmdb_data (row[0],row[1],row[2],row[3],row[4],row[5])
            else:
                print (Fore.CYAN + '____CI with sys_id: '+row[0]+' and IP address: '+row[1]+' has null password____' + Style.RESET_ALL)
                
            
            

