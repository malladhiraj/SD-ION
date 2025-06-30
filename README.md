# Prisma SD-WAN JINJA (Preview)
A script to build Primsa SD-WAN YAML files from a CSV and JINJA

#### License
MIT

#### Requirements
* Python >=3.7

#### Installation:
 Scripts directory. 
 - **Github:** Download files to a local directory, manually run the scripts. 
 - pip install -r requirements.txt

### Examples of usage:
 Please generate your API token and add it to cloudgenix_settings.py

 1. ./build.py -C demo.csv -J demo.jinja

### Caveats and known issues:
 - This is a PREVIEW release, hiccups to be expected. Please file issues on Github for any problems.

#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |


#### Pull sites
edwards-mbp-pro:cloudgenix_config aaron$ ./pull_site.py -S "MySite" --output MySite.yml 
edwards-mbp-pro:cloudgenix_config aaron$ 


#### Push sites
edwards-mbp-pro:cloudgenix_config aaron$ ./do_site.py ./MySite.yml
No Change for Site MySite.
 No Change for Waninterface Circuit to Comcast.
 No Change for Waninterface Circuit to AT&T.
 No Change for Waninterface Circuit to Megapath.
 No Change for Lannetwork NATIVE_VLAN.
 Element: Code is at correct version 5.0.1-b9.
  No Change for Element MySite Element.
   No Change for Interface 23.
   No Change for Interface 1.
   No Change for Interface controller 1.
   No Change for Interface 4.
   No Change for AS-PATH Access List test3.
   No Change for IP Community List 20.
   No Change for Routing Prefixlist test-script-list2.
   No Change for Route Map toady.
   No Change for Route Map test8.
   No Change for Route Map toady2.
   No Change for BGP Global Config 15311892501660245.
   No Change for BGP Peer teaerz.
   No Change for Staticroute 15312386843200245.
   No Change for Ntp default.
   No Change for Toolkit 15311890594020131.
No Change for Site MySite state (active).
DONE


While this script can EXTRACT a single file with ALL sites, running do_sites.py on that file is NOT RECOMMENDED.

    Best practice to do one site per config file.
        These can be automatically pulled via pull_site.py with --multi-output <directory> switch, will create a config per site.

Deletion of sites using do_site.py DESTROYS all objects under the Site. This operation is done by running do_site.py with the --destroy option. 