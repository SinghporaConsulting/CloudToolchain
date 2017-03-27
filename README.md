# cloud-toolchain
=================
Collection of scripts for common server setup tasks and DevOps automation
Easy to configure and repeatable
Continuous integration ready

---------
Contents
========

1) Shared/Scripts/SharedSetup
=============================
<<<<<<< HEAD
Consists of a maven pom that can be plugged in to CI 
Sample execute command:
 mvn initialize -DserverUsername=weblogic -DserverPassword=***** 
=======

	Consists of a maven pom that can be plugged in to CI 
	Sample execute command:
 	mvn initialize -DserverUsername=weblogic -DserverPassword=***** 
>>>>>>> 8d8e03fe077b409115b052667ae56560e8f3a8d6
		-DserverUrl=t3://pvt-c1.singhpora.com:7001 
		-DxaDSpassword=**** -DnonXADSpassword=****
		-DenvironmentCode=DEV

     Sub-configuration includes:
	a) sharedsetup/DB: Scripts and properties for creating data sources
	b) sharedsetup/DBAdapter: Script and plans for updating DBAdapter configuration
<<<<<<< HEAD
2) 
=======
2)
>>>>>>> 8d8e03fe077b409115b052667ae56560e8f3a8d6
