#!/usr/bin/env python

"""validate-vmware-login.py: Validate VMware Login"""

# libraries
# import ssl
# import requests
# from pyVim.connect import SmartConnect, Disconnect
# from pyVmomi import vim, vmodl
# import time, csv, json, jsonify, configparser, sys

__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Validate HTTP Login'
__credits__ = ['Rich Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

# # read and parse config file
# config = configparser.ConfigParser()
# config.read('config.ini')
# config.sections()

from pyVim.connect import SmartConnect
import ssl
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host="198.204.238.243", user="testuser", pwd="foobar", sslContext=s)
aboutInfo=si.content.about
 
print ("Product Name:",aboutInfo.fullName)
print("Product Build:",aboutInfo.build)
print("Product Unique Id:",aboutInfo.instanceUuid)
print("Product Version:",aboutInfo.version)
print("Product Base OS:",aboutInfo.osType)
print("Product vendor:",aboutInfo.vendor)


