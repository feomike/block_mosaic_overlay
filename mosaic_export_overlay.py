# ---------------------------------------------------------------------------
# mosaic_export_overlay.py
# Created on: May 24, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# exports the feature classes for the block table
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
theOF = "C:/Users/michael.byrne/mosaic/transfer/"
theFGDB = "C:/Users/michael.byrne/mosaic/Processing.gdb/"


#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    theFC = theFGDB + "mosaic_all"
    if arcpy.Exists(theFC):
        theCnt = int(arcpy.GetCount_management(theFC).getOutput(0))
        i = 0
        while i < theCnt:
            arcpy.AddMessage("     working on record: " + str(i + 0) + " of " + str(theCnt))
            theQry = "ObjectID = " + str(i + 1)
            theFL = "mosacicRec" + str(i + 1)
            arcpy.MakeFeatureLayer_management(theFC, theFL, theQry)
            if int(arcpy.GetCount_management(theFC).getOutput(0)) > 0:
                arcpy.CopyFeatures_management(theFL, theOF + "mosaic_" + str(i + 1) + ".shp")
            arcpy.Delete_management(theFL)
            del theQry, theFL
            i = i + 1           
except:
    arcpy.AddMessage("Something bad happened")


  
