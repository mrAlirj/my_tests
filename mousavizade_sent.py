#!/usr/bin/python3
# version: 1
from __future__ import print_function, unicode_literals
from PyInquirer import Validator, ValidationError
import validators
import ipaddress
import xmltodict
import requests
import paramiko
import time
import json
import sys
import os
import re

# value
errmsg = "Connection failed. Please Try Again."

# validators
class VlanIDValidator(Validator):
    def validate(self, document):
        try:
            val = int(document.text)
            if(val > 1 and val < 4095):
                pass
            else:
                raise ValidationError(
                    message='Please enter a valid vlan id',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            raise ValidationError(
                message='Please enter a valid vlan id',
                cursor_position=len(document.text))  # Move cursor to end

class VlanNameValidator(Validator):
    def validate(self, document):
        try:
            val = str(document.text)
            if(len(val) > 1 and len(val) < 33):
                pass
            else:
                raise ValidationError(
                    message='Please enter a valid vlan name',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            raise ValidationError(
                message='Please enter a valid vlan name',
                cursor_position=len(document.text))  # Move cursor to end
class IPSubnetValidator(Validator):
    def validate(self, document):
        try:
            val = ipaddress.IPv4Network(document.text, strict=True)
            if val.prefixlen >= 31 or val.prefixlen <= 24:
                raise ValidationError(
                    message='Please enter a valid IP subnet',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            raise ValidationError(
                message='Please enter a valid IP subnet',
                cursor_position=len(document.text))  # Move cursor to end

class HSRPIDValidator(Validator):
    def validate(self, document):
        try:
            val = int(document.text)
            if(val >= 1 and val < 256):
                pass
            else:
                raise ValidationError(
                    message='Please enter a valid hsrp id',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            raise ValidationError(
                message='Please enter a valid hsrp id',
                cursor_position=len(document.text))  # Move cursor to end

# functions
def check_prefix_list(subnets, prefixlist_dict):
    existance = []
    for seq in prefixlist_dict:
        if seq['action'] == 'permit':
            prefix = seq['rule'].split(' ')
            if len(prefix) == 1:
                if ipaddress.IPv4Network(subnets) == ipaddress.IPv4Network(prefix[0]):
                    existance.append([seq['name'], seq['seq'], ipaddress.IPv4Network(subnets)])
            elif len(prefix) == 3:
                if prefix[1] == 'le':
                    i = int(prefix[2])
                    prefix_ipaddress = []
                    while i >= ipaddress.IPv4Network(prefix[0]).prefixlen:
                        for subnet in ipaddress.IPv4Network(prefix[0]).subnets(new_prefix=i):
                            prefix_ipaddress.append(subnet)
                        i = i-1
                    if ipaddress.IPv4Network(subnets) in prefix_ipaddress:
                        existance.append([seq['name'], seq['seq'], ipaddress.IPv4Network(subnets)])
                elif prefix[1] == 'ge':
                    i = int(prefix[2])
                    prefix_ipaddress = []
                    while i <= 32:
                        for subnet in ipaddress.IPv4Network(prefix[0]).subnets(new_prefix=i):
                            prefix_ipaddress.append(subnet)
                        i = i+1
                    if ipaddress.IPv4Network(subnets) in prefix_ipaddress:
                        existance.append([seq['name'], seq['seq'], ipaddress.IPv4Network(subnets)])
            elif len(prefix) == 5:
                    i = int(prefix[2])
                    prefix_ipaddress = []
                    while i <= 32 and i >= prefix[5]:
                        for subnet in ipaddress.IPv4Network(prefix[0]).subnets(new_prefix=i):
                            prefix_ipaddress.append(subnet)
                        i = i+1
                    if ipaddress.IPv4Network(subnets) in prefix_ipaddress:
                        existance.append([seq['name'], seq['seq'], ipaddress.IPv4Network(subnets)])
    if len(existance) == 0:
        return False
    else:
        return existance

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')

def yes_no(answer):
    yes = set(['yes','y', 'ye'])
    no = set(['no','n', ''])

    while True:
        choice = input(answer).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'")

def str_to_bool(string):
    if string.lower() == 'true':
        return True
    elif string.lower() == 'false':
        return False
    else:
        raise ValueError

def ExecuteCommand(transport, pause, command):
        chan = transport.open_session()
        chan.exec_command(command)

        buff_size = 1024
        stdout = ""
        stderr = ""

        while not chan.exit_status_ready():
            time.sleep(pause)
            if chan.recv_ready():
                stdout += chan.recv(buff_size).decode('utf-8')

            if chan.recv_stderr_ready():
                stderr += chan.recv_stderr(buff_size).decode('utf-8')

        exit_status = chan.recv_exit_status()
        # Need to gobble up any remaining output after program terminates...
        while chan.recv_ready():
            stdout += chan.recv(buff_size).decode('utf-8')

        while chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size).decode('utf-8')

        stdOutStr = "\n".join(stdout.split("\n"))
        stdErrStr = "\n".join(stderr.split("\n"))

        return exit_status, stdOutStr, stdErrStr

# Send terminal length 0 to device to disable paging
def DisablePaging(RemoteConn):
    '''Disable paging on a Cisco router'''
    DisPagConf = "terminal length 0"
    ExecuteCommandOut = ExecuteCommand(RemoteConn.get_transport(), 1, DisPagConf)
    CliOutput = ExecuteCommandOut[1]

    return CliOutput

# Send Terminal NO Monitor to device to disable paging
def TerminalNOMonitor(RemoteConn):
    """Disable Monitor on a Cisco router"""
    TerminalNOMonitorConf = "terminal no monitor"
    ExecuteCommandOut = ExecuteCommand(RemoteConn.get_transport(), 1, TerminalNOMonitorConf)
    CliOutput = ExecuteCommandOut[1]

    return CliOutput

# To cheking is there route exist in routing table or NOT
def CheckRIB(Prefix, RemoteConn):

    # send ShowIpv4Route as command to device
    IPPrefix = ipaddress.ip_network(Prefix).exploded
    ShowIpv4Route = "show ip route {0}".format(IPPrefix)
    ExecuteCommandOut = ExecuteCommand(RemoteConn.get_transport(), 1, ShowIpv4Route)
    CliOutput = ExecuteCommandOut[1]

    # if my connection failed and I don't see anything even prompt!
    if CliOutput == None:
        return False
    else:
        return CliOutput




#!/usr/bin/python3
# version: 1

# import the library
from __future__ import print_function, unicode_literals
from library.pouria import NewConnection, DisablePaging, TerminalNOMonitor, Vlan, Interface, ACL, BGP, HSRP, RipeNCC, RIB, Nexus, yes_no, delete_last_line
from library.pouria import VlanIDValidator, VlanNameValidator, IPSubnetValidator, HSRPIDValidator, IPSubnetValidator
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError
from examples import custom_style_2
from termcolor import colored, cprint
from napalm import get_network_driver
from tabulate import tabulate
from getpass import getpass
from yaml import safe_load
from pprint import pprint
from sys import exit
import pandas as pd
import ipaddress
import argparse
import os

# Argument configurations
try:
    ArgParse = argparse.ArgumentParser()
    ArgParse.add_argument("-f", "--default", help="default config file", type=str, default="config/default.yml")
    ArgParse.add_argument("-v", "--verbose", help="show config output", type=bool, required=False, default=False)

except:
    print("Argument Function Failed!")
    exit(1)

ARGS = ArgParse.parse_args()

question = [
        {
            'type': 'list',
            'name': 'module',
            'message': 'Which module?',
            'choices': ['Create Customer',
            'Remove Customer',
            Separator(),
            'Show Vlan',
            'Show ARP',
            'Show MAC',
            'Show NTP',
                {
                'name': 'ping',
                'disabled': 'Unavailable at this time'
                }
            ],
            'filter': lambda val: val.upper()
        }
]

# Start
if __name__ == '__main__':
    os.system("printf '\033c'")

    # open the config file from program argument and load them as yaml
    try:
        with open(ARGS.default, 'r') as defaultfile:
            defaultcfg = safe_load(defaultfile)
    except:
        cprint("An error raising by loading the base config file. Please check your config file", "red")
        exit(1)

    answers = prompt(question, style=custom_style_2)

    RemoteConn = {}
    hostname = {}
    if answers['module'] == "SHOW ARP":
        for device in defaultcfg['connection']['device']['ip']:
            driver = get_network_driver(defaultcfg['connection']['device']['driver'])
            RemoteConn[device] = driver(device, defaultcfg['connection']['credentials']['username'], defaultcfg['connection']['credentials']['password'])
            RemoteConn[device].open()
            # get hostname
            hostname[device] = RemoteConn[device].get_facts()["hostname"]
            cprint("#################### session open to {0} ####################".format(hostname[device]), 'blue')

            get_arp_table = RemoteConn[device].get_arp_table()
            get_arp_table_df = pd.DataFrame.from_dict(get_arp_table)
            pprint(get_arp_table_df)

            #Closing the connection
            RemoteConn[device].close()
            cprint("################### SSH session closed {0} ###################".format(hostname[device]), 'blue')

        RemoteConn = {}
        hostname = {}
        for core in defaultcfg['connection']['device']['ip']:

            # Create instance of SSHClient object
            RemoteConn[core] = NewConnection(core, username=defaultcfg['connection']['credentials']['username'], password=defaultcfg['connection']['credentials']['password']).RemoteConn

            # get hostname
            hostname[core] = Nexus.hostname(RemoteConn[core])
            cprint("#################### session open to {0} #####################".format(hostname[core]), 'blue')

            # Turn off paging
            DisablePaging(RemoteConn[core])
            TerminalNOMonitor(RemoteConn[core])

            # Vlan Checking
            print("? check the existance of vlan id")
            showvlanid = Vlan.existance(basecfg['config']['vlan'], RemoteConn[core])
            if showvlanid is not False:
                vlanname = showvlanid['_readonly_']['TABLE_vlanbriefid']['ROW_vlanbriefid']['vlanshowbr-vlanname']
                vlanstate = showvlanid['_readonly_']['TABLE_vlanbriefid']['ROW_vlanbriefid']['vlanshowbr-shutstate']
                delete_last_line()
                cprint("- Vlan {0} exist and vlan name of that is {1}. State: {2}".format(basecfg['config']['vlan'], vlanname, vlanstate), end=' ')
                cprint("FAILED", "red")
                exit(1)
            else:
                delete_last_line()
                cprint("+ Vlan existance: ", end=' ')
                cprint("PASSED", "green")

            # Prefix Checking
            cprint("? check routing table:")
            for ipAddress in ipaddress.IPv4Network(basecfg['config']['hsrpsubnet']).hosts():
                routecheck = RIB.check(ipAddress, RemoteConn[core])
                delete_last_line()
                if routecheck == False:
                    cprint("FAILED", "red")
                    exit(1)
            delete_last_line()
            cprint("+ check routing table:", end=' ')
            cprint("PASSED", "green")


        if yes_no("---------- Continue? [yes, no]: ") == True:
            delete_last_line()
            cprint("++ Checking successfully ended. Configuring started", 'green')
        else:
            cprint("Stop.", "red")
            exit(1)