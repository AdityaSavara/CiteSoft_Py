# ------------------------------------------------------------------------------------------------------------
# CiteSoft
#
# Python 3.6
#
# Developer : CPH
# Date      : 06-02-2020
#
# ------------------------------------------------------------------------------------------------------------
from __future__ import print_function
from datetime import datetime
import yaml
import semantic_version
import re
import sys

def eprint(*args, **kwargs):#Print to stderr
    print(*args, file=sys.stderr, **kwargs)

_citations = {}
_OUTPUT_FILE_NAME = "CiteSoftwareCheckPoints.txt"
_CONSOLIDATED_FILE_NAME = "CiteSoftwareConsolidatedLog.txt"
_VALIDATE_OPT_ARG = True#Flag.  If set to true, argument names will be checked in real time, and invalid argument names will result in a printed warning to the user
_VALID_OPT_ARG = ["version", "cite", "author", "doi", "url", "encoding", "misc"]
_REQ_ARGS = ['timestamp', 'unique_id', 'software_name']

def module_call_cite(unique_id, software_name, **add_args):
    def inner(func):
        def call(*args, **kwargs):
            import_cite(unique_id, software_name, **add_args)
            result = func(*args, **kwargs)
            return result
        return call
    return inner

def import_cite(unique_id, software_name, **kwargs):
    add_citation(unique_id, software_name, **kwargs)


def add_citation(unique_id, software_name, **kwargs):
    new_entry = {'unique_id' : unique_id, 'software_name' : software_name, 'timestamp' : get_timestamp()}
    for key in kwargs:
        if _VALIDATE_OPT_ARG:
            if not key in _VALID_OPT_ARG:
                eprint("Warning, " + key + " is not an officially supported argument name.  Use of alternative argument names is strongly discouraged.")
        if type(kwargs[key]) is not list:#Make sure single optional args are wrapped in a list
            kwargs[key] = [kwargs[key]]
        new_entry[key] = kwargs[key]
    if unique_id in _citations:#Check for duplicate entries(e.g. from calling the same function twice)
        _citations[unique_id] = compare_same_id(_citations[unique_id], new_entry)
    else:
        _citations[unique_id] = new_entry

def compile_cite_software_log(file_path="./"):
    with open(file_path + _OUTPUT_FILE_NAME, 'a') as file:
        write_dict_to_output(file, _citations)

def consolidate_software_log(file_path="./"):
    consolidated_dict = {}
    with open(file_path + _CONSOLIDATED_FILE_NAME) as file:
        file_contents = yaml.safe_load_all(file)
        for yaml_file in file_contents:
            for item in yaml_file:
                id = item["unique_id"]
                if id in consolidated_dict:
                    consolidated_dict[id] = compare_same_id(consolidated_dict[id], item)
                else:
                    consolidated_dict[id] = item
    with open(_OUTPUT_FILE_NAME) as file:
        file_contents = yaml.safe_load_all(file)
        for yaml_file in file_contents:
            for item in yaml_file:
                id = item["unique_id"]
                if id in consolidated_dict:
                    consolidated_dict[id] = compare_same_id(consolidated_dict[id], item)
                else:
                    consolidated_dict[id] = item
    with open(_CONSOLIDATED_FILE_NAME, 'w') as file:
        write_dict_to_output(file, consolidated_dict)

#Takes a dictionary, converts it to CiteSoft-compatible YAML, and writes it to file
def write_dict_to_output(file, dictionary):
    file.write('---\r\n')
    for key,dict in dictionary.items():
        file.write('-\r\n')
        for s in _REQ_ARGS:
            file.write('    ' + s + ': >-\r\n')
            file.write('    '*2 + dict[s] + '\r\n')
        for subkey in dict:
            if subkey not in _REQ_ARGS:
                file.write('    ' + subkey + ':\r\n')
                if type(dict[subkey]) is list:
                    for i in dict[subkey]:
                        file.write('    '*2 + '- >-\r\n')
                        file.write('    '*3 + i + '\r\n')
                else:
                    file.write('    '*2 + '- >-\r\n')
                    file.write('    '*3 + dict[subkey] + '\r\n')

#Helper Functions

#Returns a string of the current time in the ISO 8601 format (YYYY-MM-DDThh:mm:ss).
def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    return timestamp

#Compares two entries
#Returns : The entry which should be kept
def compare_same_id(old_entry, new_entry):
    old_has_version = "version" in old_entry
    new_has_version = "version" in new_entry
    if old_has_version and new_has_version:#If both entries have a version, compare them return and the return the greater(newer) version
        old_ver_str = str(old_entry["version"][0])
        new_ver_str = str(new_entry["version"][0])
        #Initialize variables, assume strings are valid unless parsing fails
        old_ver_semver_valid = True
        new_ver_semver_valid = True
        decimal_regex_str = "^[0-9]+\.[0-9]+$"#Match string with decimal point enclosed by at least one number on either side
        if re.match(decimal_regex_str, old_ver_str):
            old_ver_str += '.0'#To ensure semantic version parser handles a decimal value correctly
        if re.match(decimal_regex_str, new_ver_str):
            new_ver_str += '.0'#To ensure semantic version parser handles a decimal value correctly
        try:
            old_sv = semantic_version.Version(old_ver_str)
        except ValueError:
            old_ver_semver_valid = False
        try:
            new_sv = semantic_version.Version(new_ver_str)
        except:
            new_ver_semver_valid = False
        if old_ver_semver_valid and new_ver_semver_valid:#If both entries have a valid SemVer version, keep the newer one
            if old_sv >= new_sv:
                return old_entry
            else:
                return new_entry
        elif old_ver_semver_valid:#If only the old entry has a valid SemVer version, keep it
            return old_entry
        elif new_ver_semver_valid:#If only the new entry has a valid SemVer version, keep it
            return new_entry
        else:
            #Version comparison failed, use alphanumeric comparison
            if old_ver_str > new_ver_str:
                return old_entry
            else:
                return new_entry
    elif old_has_version and not new_has_version:#If old entry has a version and the new entry doesn't, the entry with a version takes precedence
        return old_entry
    elif not old_has_version and new_has_version:#Likewise, if new entry has a version and the old entry doesn't, the entry with a version takes precedence
        return new_entry
    else:#If neither entry has a version, save the new entry
        return new_entry
