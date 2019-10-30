#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import _WellKnownEndpoint
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vm import VM

import time
import yaml
import argparse

"""
Script to execute actions against vCloud Director.

Actions:
- Authenticate with vCloud Director.
- Start virtual machines.
- Stop(shutdown) virtual machines.

Supported Virtual Machine types:

- Multiple virtual machines in different vApps.
- Multiple standalone virtual machines.

Source parameters: ./variables.yml
"""


def GetArgs():
  """
  Retrieve script arguments.
  """
  try:
     parser = argparse.ArgumentParser(
            description='Process args for starting or stopping virtual machines')
     parser.add_argument('-a', '--action', required=True, action='store',default='',
                           help="Specify 'start' or 'stop' virtual machines")
     args = parser.parse_args()
     return args
  except Exception as e:
    print("ERROR: Failed To Retrieve Arguments")
    print(e)
    exit(1)


def GetParameters(parameters_file):
  """
  Retrieve parameters from variables.yml file
  """
  try:
    print("INFO: Retrieving Parameters From " + parameters_file)

    parameters_file_contents = yaml.load(open(parameters_file), Loader=yaml.FullLoader)
    return parameters_file_contents

  except Exception as e:
    print("ERROR: Failed To Retrieve Parameters")
    print(e)
    exit(1)


def Authenticate(parameters):
  """
  Authenenticate with vCloud Director
  """
  try:
    print("INFO: Authenticating With vCloud Director")

    client = Client(parameters['VCD_HOST'],
                    api_version=parameters['VCD_API_VERSION'],
                    verify_ssl_certs=parameters['VCD_SSL_VERIFY'],
                    log_file='pyvcloud.log',
                    log_requests=True,
                    log_headers=True,
                    log_bodies=True)
    client.set_credentials(BasicLoginCredentials(parameters['VCD_USER'], parameters['VCD_ORG'], parameters['VCD_PASSWORD']))
    return client

  except Exception as e:
    print("ERROR: Failed To Authenticate With vCloud Director")
    print(e)
    exit(1)


def GetvAppObj(parameters, client, virtual_machine):
  """
  Get vApp Object
  """
  try:

    # Get the org object that corresponds with the org provided at runtime
    org_resource = client.get_org()
    org = Org(client, resource=org_resource)

    #  Get the VDC object that correspondes with the VDC provided at runtime
    vdc_resource = org.get_vdc(parameters['VCD_VDC'])
    vdc = VDC(client, resource=vdc_resource)

    # Loop through all vApps until matching virtual machine is found, return vapp
    vapps = vdc.list_resources(EntityType.VAPP)
    for vapp in vapps:
      vapp_name = vapp.get('name')
      vapp_resource = vdc.get_vapp(vapp_name)
      vapp = VApp(client, resource=vapp_resource)

      for vm in vapp.get_all_vms():
        if vm.get('name') == virtual_machine:
           return vapp

  except Exception as e:
    print("ERROR: Failed To Get vApp Object For Virtual Machine: '" + virtual_machine + "'")
    print(e)
    exit(1)

def StartVMs(parameters, client):
  """
  Start Virtual Machines
  """
  try:

    for virtual_machine in parameters['VIRTUAL_MACHINES']:
      vapp = GetvAppObj(parameters, client, virtual_machine)
      vm_resource = vapp.get_vm(virtual_machine)
      vm = VM(client, resource=vm_resource)

      state = vm.get_power_state()
      if state == 4:
        print("INFO: VM '" + virtual_machine + "' Already Powered On")
      elif state == 8:
        print("INFO: Starting VM: '" + virtual_machine + "'")
        vm.power_on()
      else:
        print("INFO: VM '" + virtual_machine + "' In Unknown State, No Action Taken")

  except Exception as e:
    print("ERROR: Failed To Start VM: '" + virtual_machine + "'")
    print(e)
    exit(1)


def StopVMs(parameters, client):
  """
  Shutdown Virtual Machines
  """
  try:

    for virtual_machine in parameters['VIRTUAL_MACHINES']:
      vapp = GetvAppObj(parameters, client, virtual_machine)
      vm_resource = vapp.get_vm(virtual_machine)
      vm = VM(client, resource=vm_resource)

      state = vm.get_power_state()
      if state == 8:
        print("INFO: VM '" + virtual_machine + "' Already Powered Off")
      elif state == 4:
        print("INFO: Shutting Down VM: '" + virtual_machine + "'")
        vm.shutdown()
      else:
        print("INFO: VM '" + virtual_machine + "' In Unknown State, No Action Taken")

  except Exception as e:
    print("ERROR: Failed To Shutdown VM: '" + virtual_machine + "'")
    print(e)
    exit(1)

def main():
  """
  Command-line program to stop(shutdown) or start virtual machines in vCloud Director.
  """
  try:

    now = time.strftime("%c")
    ## date and time
    print("Starting: " + time.strftime("%c"))

    args = GetArgs()
    parameters_file = './variables.yml'
    parameters = GetParameters(parameters_file)
    client = Authenticate(parameters)

    if args.action == 'stop':
      StopVMs(parameters, client)
    elif args.action == 'start':
      StartVMs(parameters, client)
    else:
      print("ERROR: Unknown Action, Only 'start' or 'stop' Supported, Exiting..")
      exit(1)

    # Log out.
    print("Logging out")
    client.logout()

    print("Complete: " + time.strftime("%c"))
    return 0
  except Exception as e:
    print("ERROR: Failed To Execute Script")
    print(e)
    exit(1)

# Start program
if __name__ == "__main__":
   main()
