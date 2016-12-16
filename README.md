# cloud-toolchain
Collection of scripts for common server setup tasks
Easy to configure and repeatable
Continuous integration ready

---------
Contents
---------

1) Shared/Scripts/SharedSetup
Consists of a maven pom that can be plugged in to CI 
Sample execute command:
 mvn initialize -DserverUsername=weblogic -DserverPassword=***** 
		-DserverUrl=t3://pvt-c1.singhpora.com:7001 
		-DXADSpassword=**** -DNonXADSpassword=****
		-DenvironmentCode=DEV

2) 