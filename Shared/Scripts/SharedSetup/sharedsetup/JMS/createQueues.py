"""
This script starts an edit session, creates a JMS persistent store, JMS Server
and queues using setup information in the properties file supplied as argument
Sample run command:
wlst createQueues.py weblogic ******* t3://localhost:7001 ./CONFIG/Sample1JMSModule_DEV.properties
(or set it up in the project level pom file to execute via maven wlst plugin)
"""


# Author Jang-Vijay Singh
# Date 1/6/2016

import sys
from java.lang import System



username = sys.argv[1]
password = sys.argv[2]
#url Format: 't3://' + sys.argv[1] + ':' + sys.argv[2]
url = sys.argv[3]

#
properties_file = sys.argv[4]

def main():
  #
  # Create a JMS Module with Queues
  #
    print ">>>Load createQueues ..."

    #================================
    # Properties File Location
    #================================
    print('>>> loading properties '+ properties_file)
    properties = loadProperties(properties_file)
    ######Read properties
    modulePrefix=prop_modulePrefix
    jndiPrefix=prop_jndiPrefix
    cfName=prop_cfName
    cfXAEnabled = prop_cfXAConnectionFactoryEnabled
    queueName=prop_queueName

    connect(username, password, url)

    #
    edit()
    startEdit()

    servermb=getMBean("Servers/"+"AdminServer")

    if servermb is None:
        print 'Target cluster JMS_Cluster not found ...'

    else:
        print servermb
        try:
          print "Create File Store"
          fileStore1 = create(modulePrefix+'FileStore1', 'FileStore')
          fileStore1.addTarget(servermb)
          fileStore1.setDirectory('/tmp')


          print ">>>Creating JMS Servers..."
          jmsserver1mb = create(modulePrefix+'JMSServer1','JMSServer')
          jmsserver1mb.addTarget(servermb)
          jmsserver1mb.setPersistentStore(fileStore1)

          print ">>>Creating JMS Module..."
          jmsMySystemResource = create(modulePrefix+"Module","JMSSystemResource")
          jmsMySystemResource.addTarget(servermb)

          subdeploymentName=modulePrefix+'SubDeployment'
          print ">>>Creating SubDeployment.."+ subdeploymentName
          subDep1mb = jmsMySystemResource.createSubDeployment(subdeploymentName)
          subDep1mb.addTarget(jmsserver1mb)


          theJMSResource = jmsMySystemResource.getJMSResource()

          print ">>>Creating Connection Factory..." + modulePrefix+cfName
          connfact1 = theJMSResource.createConnectionFactory(modulePrefix+cfName)
          connfact1.setJNDIName(jndiPrefix + '.' + cfName)
          connfact1.setDefaultTargetingEnabled(true)

          try:
            cfXAConnectionFactoryEnabled=cfXAEnabled
            print ">>> Setting XA to true for the connection factory..."
            cd('/JMSSystemResources/' +modulePrefix+"Module"+'/JMSResource/'+modulePrefix+"Module"+
                    '/ConnectionFactories/' + modulePrefix+cfName + '/TransactionParams/' +modulePrefix+cfName)
            cmo.setXAConnectionFactoryEnabled(bool(cfXAConnectionFactoryEnabled))
          except:
            print ">>> Did not set XA to true for the connection factory..."



          print "->>> Creating queue..." + queueName
          jmsqueue1 = theJMSResource.createQueue( queueName)
          jmsqueue1.setJNDIName(jndiPrefix+'.'+queueName)
          jmsqueue1.setSubDeploymentName( subdeploymentName  )
        except:
          print "ERROR  "

    try:
        save()
        activate(block="true")
        print "script returned SUCCESS"
    except:
        print "ERROR. "
        dumpStack()

main()