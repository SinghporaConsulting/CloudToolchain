"""
This script is used to deploy the DBAdapter to weblogic using a configuration plan. 
The configuration plan itself can be externally managed, source controlled and promoted across 
    environments. 
Managing it in source control avoids conflicting setup and provides 
    visibility on what setup exists on a given target environment

The required arguments, including the enviornment specific adapter plan 
    can be supplied via the environment. (see execution ID WLST_updateDBAdapter 
    in the pom file associated with this project)
"""
#
# Author Jang-Vijay Singh
# Singhpora Consulting #NimbleEfficientAgile
# www.singhpora.com 
# Date 01/06/2016

import sys
from java.lang import System

username = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
planLocation =  sys.argv[4]
 

def main():
    connect(username,password,url)
    name = 'DbAdapter'

    print "Creating DB adapter resource  information"
    try:
         redeploy(name, planLocation, upload='true', stageMode='stage') 
        
    except:
        print "Error while modifying db adapter connection factory"
main()