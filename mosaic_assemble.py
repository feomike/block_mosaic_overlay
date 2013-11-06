# ---------------------------------------------------------------------------
# mosaic_assemble.py
# Created on: March 8, 2013
# Created by: Michael Byrne
# Federal Communications Commission
# assembles the mosaic data into one dataset
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math


#write out global variables
thePGDB = "C:/Users/michael.byrne/mosaic/processing.gdb"  #processing file geodatabase
arcpy.env.workspace = thePGDB
theLocation = "K:/Projects/Broadband Data/SWAT/American Roamer/2013 Jan/Carriers/"
#theLocation = "C:/Users/michael.byrne/mosaic/Carriers/test/"
theSpatialRef = "C:/Users/michael.byrne/mosaic/mosaic.prj"
CleanFirst = "yes"

if CleanFirst == "yes":
    #clean files first
    myFCs = ["mosaic_all"]
    for myFC in myFCs:
        if arcpy.Exists(myFC):
            arcpy.Delete_management(myFC)
    #create a new blank mosaic dataset
    arcpy.CreateFeatureclass_management(thePGDB, "mosaic_all", "POLYGON", thePGDB + "/mosaic_template", "", "", theSpatialRef)

 
##write out functions
##function to assemble the right directories of delivered files
def mosaic_files():
    #clean files first
    myFCs = ["mydata", "mydata_dis"]
    for myFC in myFCs:
        if arcpy.Exists(myFC):
            arcpy.Delete_management(myFC)

    # get the list of the shape files in that directory
    for dirname, dirnames, filenames in os.walk(theLocation):
        for filename in filenames:
            #print os.path.join(dirname, filename)
            #arcpy.AddMessage(os.path.join(dirname, filename))
            #arcpy.AddMessage("the right side is: " + os.path.join(dirname, filename)[-4:])
            if os.path.join(dirname, filename)[-4:] == ".shp":
                arcpy.AddMessage("thefile is: " + os.path.join(dirname, filename))
                #copy in the source shapefile as the featureclass mydata
                arcpy.CopyFeatures_management (os.path.join(dirname, filename), thePGDB + "/mydata")
                #repair geometry on this
                arcpy.RepairGeometry_management(thePGDB + "/mydata")
                #create a new mydata featureclass which is a dissolve of the fields in the input shp
                arcpy.Dissolve_management("mydata", thePGDB + "/mydata_dis", ["mkg_name", "entity", "protocol"])
                #append the mydata featureclass to mosaic_all featureclass
                arcpy.Append_management (["mydata_dis"], "mosaic_all") #, {schema_type}, {field_mapping}, {subtype})
                myFCs = ["mydata", "mydata_dis"]
                for myFC in myFCs:
                    if arcpy.Exists(myFC):
                        arcpy.Delete_management(myFC)
    return()


#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    if arcpy.Exists(thePGDB + "/mosaic_all"):
         mosaic_files()
         #open a file to write when it finished
         #outFile = "C:/users/michael.byrne/706/wireless_overlay_" + theST + ".txt"
         #myFile = open(outFile, 'w')
         #myFile.write(theST + ": finished\n")
         #myFile.close()
    else:
         arcpy.AddMessage("output feature class doesn't exist")
    del theLocation, theSpatialRef
except:
    arcpy.AddMessage("Something bad happened")


  
