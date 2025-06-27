#!/usr/bin/env python3
import argparse
import yaml
import sys
import logging
import os
import datetime
import sys
import csv
import jinja2
import requests
import urllib3
urllib3.disable_warnings()



# Global Vars
SCRIPT_NAME = 'CloudGenix: Shutdown ION'
SCRIPT_VERSION = "1"

# Set NON-SYSLOG logging to use function name
logger = logging.getLogger(__name__)

####################################################################
# Read cloudgenix_settings file for auth token or username/password
####################################################################


def build(list_of_csv, jinja): 
    local = os.getcwd()
    path = "site-files"
    isExist = os.path.exists(path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(path)
       print("The new directory site-files is created!")
    for site in list_of_csv:
        if "site_name" not in site:
            print("site_name is a required field please update your csv and jinja")
            return
        address_concat = ""
        if "street" in site:
            address_concat = site['street']
        if "city" in site:
            address_concat += ", " + site['city']
        if "state" in site:   
            address_concat += ", " + site['state'] 
        if "post_code" in site:
            address_concat += ", " + site['post_code'] 
        if "country" in site:    
            address_concat += ", " + site['country']
        if address_concat != "":
            address_concat = address_concat.strip()
            # Geocoding disabled
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=local))
        template = env.get_template(jinja)
        result = template.render(site)
        f = open(os.path.join(path, site['site_name'] + ".yaml"), "w")
        f.write(result)
        f.close()
        print("Built site " + site['site_name'])
    return
                                 
def go():
    ############################################################################
    # Begin Script, parse arguments.
    ############################################################################
    # Parse arguments
    parser = argparse.ArgumentParser(description="{0}.".format(SCRIPT_NAME))
    # Allow Controller modification and debug level sets.
    config_group = parser.add_argument_group('Name', 'These options change how the configuration is loaded.')
    config_group.add_argument("--csv", "-C", help="Site list file", required=True, default=None)
    config_group.add_argument("--jinja", "-J", help="Site list file", required=True, default=None)
    args = vars(parser.parse_args())
    # get time now.
    curtime_str = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d-%H-%M-%S')
    site_list = args["csv"]
    jinja = args["jinja"]
    list_of_csv = []
    with open(site_list, 'r') as data:
      for line in csv.DictReader(data):
          list_of_csv.append(line)
    build(list_of_csv, jinja) 
    # end of script

if __name__ == "__main__":
    go()