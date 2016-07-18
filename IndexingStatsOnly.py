# ArchiveAndCompress.py
# Archive and Compress by Corey White and Carl Stearns. Raleigh Public Utilities GIS 2014/08/25
###########################################################################################################
# Import arcpy, os, datetime modules
import arcpy, os, datetime, sys
from arcpy import env
arcpy.env.overwriteOutput = True
###########################################################################################################

def Archive():

    #set workspace
    arcpy.env.workspace = "Database Connections\\RPUD.sde" # Need to change this to work where it runs
    print "workspace set"
    #list of datasets to archive
    datasetList = ["RPUD.EVENTS","RPUD.ProjectTracking","RPUD.PU_Boundaries","RPUD.ReclaimedWaterDistributionNetwork","RPUD.Sewer_Features","RPUD.SewerCollectionNetwork","RPUD.WaterDistributionNetwork", "RPUD.Water_Distribution_Features"]
    print "dataset list compiled"
    #date string for geodb name
    dateString = datetime.datetime.now().strftime("%Y%m%d")
    print "date string created"
    #create file geodb
    arcpy.CreateFileGDB_management("//corfile/Public_Utilities_NS/5215_Capital_Improvement_Projects/636_Geographic_Info_System/Archive/", "RPUD" + dateString+ ".gdb") #will security settings on this directory prevent copy? If so go \\corfile\Common
    print "file geodatabase created"
    #copy datasets to Archive
    for dataset in datasetList:
        print "archiving " + dataset
        arcpy.Copy_management(dataset, "//corfile/Public_Utilities_NS/5215_Capital_Improvement_Projects/636_Geographic_Info_System/Archive/" + "RPUD" + dateString+ ".gdb/" + dataset ) #will security settings on this directory prevent copy? If so go \\corfile\Common
    print "Archiving complete"

#Archive()

###################################################################################################################################################################################################################################

def Compress():
    #set workspace
    sde = "Database Connections/sdeadmin.sde"
    RPUDwkspace = "Database Connections/RPUD_TESTDB.sde"
    arcpy.env.workspace = sde


    #list versions
    #versionList = [version.name for version in arcpy.da.ListVersions(RPUDwkspace) if version.isOwner and version.name != 'SDE.DEFAULT']

    #print "These are the current versions: %s" % versionList

    # get time for naming log file
    #ReconcileTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    #filePath = "C:/Users/stearnsc/Junk/Reconcile{0}.txt".format(ReconcileTime)

    #reconcile, post and delete versions
    #arcpy.ReconcileVersions_management(RPUDwkspace,"ALL_VERSIONS","SDE.DEFAULT",versionList,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","POST","DELETE_VERSION",filePath)
    #print "Reconcile, Post and Delete is Complete"


    # perform compression
    #print "Starting compression"
    #arcpy.Compress_management("Database Connections\\sdeadmin.sde")
    #print "Compression is Complete"

    #change workspace to RPUD
    arcpy.env.workspace = RPUDwkspace

    #Analyze Datasets#
    #list tables & feature classes
    print 'Creating list of of tables and features to index and analyze'
    tables = [t for t in arcpy.ListTables() if 'RPUD.' in t]
    fc = [f for f in arcpy.ListFeatureClasses() if 'RPUD.' in f]
    dataList = tables + fc
    removeList = ['RPUD.IWOS_MANUFACTURERS_VIEW','RPUD.IWOS_ASSETS_VIEW', 'RPUD.GIS_CREATES', 'RPUD.GIS_UPDATES']
    # Removes tables that cannot be indexed or analyzed
    for each in removeList:
      dataList.remove(each)

    versionList = ['MMAZANEK_VERSION', 'DTISKA_VERSION', 'SKAUFMAN_VERSION', 'CSTEARNS_VERSION', 'JKELLER_VERSION', 'ABAILEY_VERSION', 'JSORRELL_VERSION', 'EGREEN_VERSION']

    #run Rebuild Indexes tool
    arcpy.RebuildIndexes_management(sde, "SYSTEM", dataList, "ALL")
    print 'Rebuild Indexes Complete'

    #run Analyze Datsets tool
    arcpy.AnalyzeDatasets_management(sde, "SYSTEM", dataList, "ANALYZE_BASE","ANALYZE_DELTA","NO_ANALYZE_ARCHIVE") #currently we do not have archiving enabled, but we should
    print "Analyze Complete"



    #re-create versions
    #print "Recreating Versions"
   # for version in versionList:
    #  arcpy.CreateVersion_management(RPUDwkspace, "SDE.DEFAULT", version, "PUBLIC")
   # print "Versions re-created. Go get a beer."
    print "indexing & statistics complete"
Compress()

###################################################################################################################################################################################################################################
