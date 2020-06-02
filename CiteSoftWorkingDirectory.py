#------------------------------------------------------------------------------------------------------------
# Cite Soft
#
# Python 3.6
#
# Developer : CPH
# Date      : 06-02-2020
#
#------------------------------------------------------------------------------------------------------------
from datetime import datetime
import yaml

_citations = {}
_OUTPUT_FILE_NAME = "CiteSoftwareCheckPoints.txt"
_CONSOLIDATED_FILE_NAME = ""

def module_call_cite(func, unique_id, software_name, **kwargs):
    def inner(unique_id, software_name, **kwargs):
        import_cite(unique_id, software_name, kwargs)
        func()
    return inner

def import_cite(unique_id, software_name, **kwargs):
    add_citation(unique_id, software_name, kwargs)


def add_citation(unique_id, software_name, **kwargs):
    new_entry = {'unique_id' : unique_id, 'software_name' : software_name, 'timestamp' : getTimestamp()}
    for key in kwargs:
        new_entry[key] = kwargs[key]
    if unique_id in citations:#Check for duplicate entries(e.g. from calling the same function twice)
        pass#For now, do nothing
    else
        citations[unique_id] = dict

def compile_cite_software_log():
    for()

def consolidate_software_log():
    with open(_OUTPUT_FILE_NAME) as file:
        file_contents = yaml.safe_load(file)

#Helper Functions

#Returns a string of the current time in the ISO 8601 format (YYYY-MM-DDThh:mm:ss).
def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    return timestamp

def compare_same_id(old_entry, new_entry):
    old_has_verison = "version" in old_entry
    new_has_version = "version" in new_entry
    if old_has_version and new_has_version:#If both entries have a version, compare them return and the return the greater(newer) version
        if old_entry["version"] > new_entry["version"]:
            return old_entry
        else:
            return new_entry
    elif old_has_version and not new_has_version:#If old entry has a version and the new entry doesn't, the entry with a version takes precedence
        return old_entry
    elif not old_has_version and new_has_version:#Likewise, if new entry has a version and the old entry doesn't, the entry with a version takes precedence
        return new_entry
    else:#If neither entry has a version, don't replace the existing entry
        return old_entry
