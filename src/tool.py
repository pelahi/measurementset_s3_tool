#!/usr/bin/env python
"""

Setup script for .

"""

import os
import sys
import subprocess
import casacore
import boto3
import pylut

def MeasurementSetMeta(set: str):
    """
    @brief Extract metadata for measurement set residing on POSIX filesystem 
    
    @param set : measurement set name
    """
    meta = dict()

    return meta 

def MeasurmentSetTarandMeta(
    set : str,
    tarname : str,
    lustrestriping : str = "-c 16 -S 4M", 
    icompress : bool = True, 
):
    """
    @brief tar a measurement set that exists on a LUSTER filesystem
    extract metadata and return dictionary of information 
    
    @param set : measurement set name
    @param tarname : tar filename to be produced
    @param lusterinfo : striping to use when producing tar file 
    @param icompress : whether or not to compress data 

    @return measurementset_info : dictionary containing metadata and also tar files ready to be uploaded to object store
    """

    # get metadata for S3 
    meta = MeasurmentSetMeta(set)

    measurementset_s3_info = dict()

    # set the tar name and commmand 
    tarsuffix = ".tar"
    tarargs = "cf"
    if icompress:
        tarsuffix=".tgz"
        tarargs="zcf"
    
    # tar file for metadata 
    smallname= tarname+".meta" + tarsuffix
    largename= tarname+".set" + tarsuffix
    
    # create a highly stripped tar file(s)
    cmd="lfs setstripe " + smallname
    subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ( output, errput ) = subp.communicate()

    # search for all small files within the directory that should contain metadata 
    cmd="find " + set + "-type f -size -1M"
    subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ( smallfiles, errput ) = subp.communicate()
    # and all larger files 
    cmd="find " + set + "-type f -size +1M"
    subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ( largefiles, errput ) = subp.communicate()

    # then generate tar files 
    cmd="tar " + tarargs + " " + smallname + " " + smallfiles 
    subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ( output, errput ) = subp.communicate()

    return measurementset_s3_info

def MeasurementSetMove(
    local_set : str, 
    remote_set : str,
    local : str, 
    remote : str
    ):
    """
    @brief Move a measurement set from a local to a remote 

    @param local_set : string of local measurement set name
    @param remote_set : string of remote object name(s) 
    @param local : string of either posix path or remote object store 
    @param remote : string of either remote object store 
    """
    
