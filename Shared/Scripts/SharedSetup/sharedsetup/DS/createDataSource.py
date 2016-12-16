import time

# Generic and adaptable script to create a data source. 
#
# Pass the appropriate properties file as argument
# parameters below need to be supplied in order from the command line. 
# TODO - 1) break down into smaller functions
#        2) Conditionally use properties instead of username/password for server connection 
##########Jang-Vijay Singh
##########6 June 2016

# username to connect to the admin server
username             = sys.argv[1]
# password to connect to the admin server
# Use a proper password plugin if supplying from Jenkins/hudson
password             = sys.argv[2]

# admin server url (e.g. t3://localhost:7001)
url                  = sys.argv[3]

# the database password
# Use a proper password plugin if supplying from Jenkins/hudson
dbPassword           = sys.argv[4]
# the environment code (DEV, SIT, UAT, PROD)
properties_file = sys.argv[5]

try:
    isGridLink = sys.argv[6]
except:
    isGridLink = false;
    print '---> Assuming this is NOT a gridlink data source as arg[6] was false or blank'

def main():

  #
  # Create a JDBC Data Source.
  #
  try:
  
    #================================
    # Properties File Location
    #================================
    print(' Loading properties '+ properties_file)
    properties = loadProperties(properties_file)
    
    ######Load properties
    dsName=__dsName
    jndiName=__jndiName
    dbUrl=__dbUrl
    dbUser=__dbUser
    dbDriver=__dbDriver

        
    initCapacity = __InitCapacity
    testTableValue = __TestTable

    #Optional properties begin here
    try:
      ONS_WALLET_FILE=__ONS_WALLET_FILE
    except:
      ONS_WALLET_FILE=''
    try:
      ONS_NODE_LIST=__ONS_NODE_LIST
    except:
      ONS_NODE_LIST=''
      
    try:
      globalTxProtocol=__GlobalTxProtocol
    except:
      globalTxProtocol='none'
    
    try:
      minCapacity=__MinCapacity
    except:
      print '--> Defaulting minCapacity to 1 '
      minCapacity=1
    
    try:
      maxCapacity=__MaxCapacity
    except:
      print '--> Defaulting maxCapacity to 15 '
      maxCapacity=15
      
    #optional properties used only by some data sources
    try:
      databaseName=__databaseName
    except:
      databaseName=''
    try:
      portNumber=__portNumber
    except:
      portNumber=''
    
    #optional properties end here
    
    print('--> Setup loaded about to connect to weblogic with user ' + username)
    connect(username, password, url)
    

    cd('/')
    nonXADS = getMBean("/JDBCSystemResources/"+dsName)
    edit()
    startEdit()    
    if nonXADS is None:  
      print '--->Creating DataSource: ' +dsName   
    else:
      print '---> delete existing data source and re-creatign a new one -' + dsName
      cd('/')
      print "Deleting datasource: " + dsName
      delete(dsName,'JDBCSystemResource')
      save()
      activate()
      edit()
      startEdit()   
      print '---> deleted existing ' + dsName

    
    cmo.createJDBCSystemResource(dsName)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
    cmo.setName(dsName)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    set('JNDINames',jarray.array([String(jndiName)], String))
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
    cmo.setUrl(dbUrl)
    cmo.setDriverName(dbDriver)
    cmo.setPassword(dbPassword)
      
    print '--->Created data source... Setting or updating properties now '
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
    cmo.setTestTableName('DUAL')
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
    cmo.createProperty('user')
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
    cmo.setValue(dbUser)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    cmo.setGlobalTransactionsProtocol(globalTxProtocol)
    
    ###These are the properties in the box in the Connection Pool tab
    if databaseName != '' :
      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
      cmo.createProperty('databaseName')
      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/databaseName')
      cmo.setValue(databaseName)
      print 'explicit databaseName property was set ' + databaseName
    if portNumber != '' :
      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
      cmo.createProperty('portNumber')
      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/portNumber')
      cmo.setValue(portNumber)
      print 'explicit portNumber property was set ' + portNumber
    

    ## CONNECTION POOL CONFIGURATION ##
    print '---> Applying connection pool properties'
    cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCConnectionPoolParams/'+dsName)    
    cmo.setInitialCapacity(int(initCapacity))       
    try:
        cmo.setMinCapacity(int(minCapacity))       
    except:
        print '--> Did not set minCapacity '
        
    try:
        cmo.setMaxCapacity(int(maxCapacity))       
    except:
        print '--> Did not set maxCapacity '
        
    cmo.setTestConnectionsOnReserve(true)	    
    cmo.setConnectionCreationRetryFrequencySeconds(10)
    
    cmo.setTestTableName(testTableValue)
    
    try:
      JDBCReadTimeout = __JDBCReadTimeout
      print '---> found JDBCReadTimeout: ' + JDBCReadTimeout
      cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName+'/Properties/'+dsName)
      cmo.createProperty('oracle.jdbc.ReadTimeout')
          
      cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName+'/Properties/'+dsName+'/Properties/oracle.jdbc.ReadTimeout')
      cmo.setValue(JDBCReadTimeout)
    except:
      print '---> skipping JDBCReadTimeout - no value found '
    
    print('--> Setting or updating gridlink properties if available')
    
    ## GridLink Specific Config
    cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCOracleParams/'+dsName)
    
    cmo.setFanEnabled(bool(isGridLink))
    cmo.setOnsWalletFile(ONS_WALLET_FILE)
    cmo.unSet('OnsWalletPasswordEncrypted')
    cmo.setOnsNodeList(ONS_NODE_LIST)
        
    print('--> setting targets')
    cd('/JDBCSystemResources/' + dsName)

    try:
      targetClusterName = __targetClusterName
      set('Targets',jarray.array([ObjectName('com.bea:Name=' + targetClusterName + ',Type=Cluster')], ObjectName))
      print '--> Set TargetCluster to ' + targetClusterName
    except:
      print '--> Did not set TargetCluster '
    save()
    print('--> activating changes')
    activate()
    print('--> done')      
    
    print "********************************************************************"
    print "***** Datasource "+dsName+ " was created or updated now "
        
  except:
    dumpStack()
    print('-->ERROR something went wrong, bailing out - verify the setup manually or check previous log entries.')
    edit()
    stopEdit('y')
    disconnect('y')
    raise SystemExit

  #
  # disconnect from the admin server
  #

  print('--> disconnecting from admin server now')
  disconnect()

#This is the main entry point
main()
