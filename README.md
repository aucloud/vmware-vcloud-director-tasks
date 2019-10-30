# VMware vCloud Director Tasks

This project contains python scripts to interact with the vCloud Director API to carry out specific tasks.

Supported tasks:

  - Stop virtual machines
  - Start virtual machines

This project uses the pycloud Python SDK to interact with the vCloud Director API.

Alternatively you can use the Python vcd-cli, however this is not covered in this project. See reference material below for more information.

## Prerequisites

* Python3 >= v3.7.3
* pyvcloud Python SDK >= v21.0.0

## Project Contents

* variables.yml - Contains credentials, connection information and virtual machines to manage.
* VMAction.py - Script to start or stop virtual machines specified in the variables file.

### Installation

See: https://github.com/vmware/pyvcloud/blob/master/docs/install.md

## Usage

The following provides instructions on how to use this project.

### Authentication

To authenticate with the vCD API populate the below entries in the variables.yml file.

  ```
  VCD_HOST: '< vCloud Director hostname or ip >'
  VCD_SSL_VERIFY: < True or False >
  VCD_API_VERSION: '< vCloud Director API version >'
  VCD_ORG: '< vCloud Director vOrg friendly name >'
  VCD_VDC: '< vCloud Director vDC name >'
  VCD_USER: '< vCloud Director username >'
  VCD_PASSWORD: '< vCloud Director password >'
  ```
Example:

  ```
  VCD_HOST: 'https://my-portal.com.au'
  VCD_SSL_VERIFY: True
  VCD_API_VERSION: '31.0'
  VCD_ORG: 'test-vorg'
  VCD_VDC: 'test-vdc'
  VCD_USER: '40.0'
  VCD_PASSWORD: 'password'
  ```  

To retrieve the "VCD_API_VERSION" browse to "VCD_HOST"/api/versions and search for the latest version.

To retrieve the "VCD_ORG" login to the vCloud Director UI, select "Administration" from the top drop down menu, then select "General". You will then see your "Organization name".

To retrieve the "VCD_VDC" login to the vCloud Director UI, select "Datacenters" from the top drop down menu, then under "Virtual Datacenters" find the name of your vDC.

To retrieve the "VCD_USER" login to the vCloud Director UI, select "Administration" from the top drop down menu, then select "Users" and find the "Name" matching the users "Full Name".

### Stopping & Starting Virtual Machines

Virtual machines can either created as a standalone virtual machine that has a system generated vApp, or a virtual machine under a user created vApp. This script supports both options by retrieving the vApp name, therefore you do not need to specify the vApp name only the virtual machine name on single quotes.

In order to stop or start virtual machines populate the below entry in the variables.yml file.

  ```
  VIRTUAL_MACHINES:
     - '< virtual machine name >'
     - '< virtual machine name >'
  ```
Example:

  ```
  VIRTUAL_MACHINES:
     - 'server 01'
     - 'server 02'
  ```

To start virtual machines run:

  ```
  python3 VMAction.py -a start
  ```

To stop virtual machines run:

  ```
  python3 VMAction.py -a stop
  ```

The stop action will "shutdown" a virtual server by shutting down the guest operating system.  

## Material

* https://vmware.github.io/pyvcloud/index.html
* https://vmware.github.io/vcd-cli/
