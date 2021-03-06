"""
PSFex wrapper for python
"""
from __future__ import print_function, division
from toyz.utils.errors import ToyzError
import subprocess
import os

class AstroPsfexError(ToyzError):
    pass

def get_version():
    """
    Parse output for Sextractor version and date
    """
    try:
        p = subprocess.Popen('psfex', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except:
        raise AstroPsfexError("Unable to run PSFex. "
            "Please check that it is installed correctly")
    for line in p.stdout.readlines():
        line_split = line.split()
        line_split = map(lambda x: x.lower(), line_split)
        if 'version' in line_split:
            version_idx = line_split.index('version')
            version = line_split[version_idx+1]
            date = line_split[version_idx+2]
            break
    return version, date

def run_psfex(filenames, temp_path, config, config_file=None, store_output=False,
        psfex_cmd='psfex'):
    """
    Run PSFex given a set of config options
    """
    import toyz.utils.core
    import os.path
    
    # If a single catalog is passed, convert to an array
    if not isinstance(filenames, list):
        filenames = [filenames]
    
    # If the user specified a config file, use it
    if config_file is not None:
        psfex_cmd += ' -c '+config_file
    # Add on any user specified parameters
    for param in config:
        if isinstance(config[param], bool):
            if config[param]:
                val='Y'
            else:
                val='N'
        else:
            val = config[param]
        psfex_cmd += ' -'+param+' '+val
    
    # Run PSFex
    for f in filenames:
        this_cmd = psfex_cmd+' '+f
        print(this_cmd, '\n')
        if store_output:
            p = subprocess.Popen(this_cmd, shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
        else:
            subprocess.call(this_cmd, shell=True)
    
    status =  'success'
    
    if store_output:
        output = p.stdout.readlines()
        for line in output:
            if 'error' in line.lower():
                status = line
                break
    
    return status