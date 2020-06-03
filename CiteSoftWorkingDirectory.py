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
import semantic_version
import re

#Dependencies for testing only
from random import randint

_citations = {}
_OUTPUT_FILE_NAME = "CiteSoftwareCheckPoints.txt"
_CONSOLIDATED_FILE_NAME = "CiteSoftwareConsolidatedLog.txt"

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
    new_entry = {'unique_id' : unique_id, 'software_name' : software_name, 'timestamp' : get_timestamp(), 'version' : '1.00'}
    for key in kwargs:
        new_entry[key] = kwargs[key]
    if unique_id in _citations:#Check for duplicate entries(e.g. from calling the same function twice)
        _citations[unique_id] = compare_same_id(_citations[unique_id], new_entry)
    else:
        _citations[unique_id] = new_entry

def compile_cite_software_log():
    with open(_OUTPUT_FILE_NAME, 'a') as file:
        write_dict_to_output(file, _citations)

def consolidate_software_log():
    consolidated_dict = {}
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
        for s in {'timestamp', 'unique_id', 'software_name', 'version'}:
            file.write('    ' + s + ': >-\r\n')
            file.write('    '*2 + dict[s] + '\r\n')
        for subkey in dict:
            if subkey not in {'timestamp', 'unique_id', 'software_name', 'version'}:
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
        old_ver_str = old_entry["version"]
        new_ver_str = new_entry["version"]
        try:
            old_sv = semantic_version.Version(old_ver_str)
            new_sv = semantic_version.Version(new_ver_str)
            if old_sv > new_sv:
                return old_entry
            else:
                return new_entry
        except ValueError:
            regex = "[0-9]*\.[0-9]*"
            if re.match(regex, old_ver_str) and re.match(regex, new_ver_str):
                try:
                    old_ver_float = float(old_ver_str)
                    new_ver_float = float(new_ver_str)
                    if old_ver_float > new_ver_float:
                        return old_entry
                    else:
                        return new_entry
                except ValueError:
                    if old_ver_str > new_ver_str:
                        return old_entry
                    else:
                        return new_entry
            else:
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

def main():
    print("Welcome to CiteSoft!")
    print("Running test cases...")
    test_inline_citation()
    test_wrapper_func()
    test_semantic_version()
    test_decimal_version()
    print("Appending citations to data file")
    compile_cite_software_log()
    consolidate_software_log()

#Test Cases
def test_inline_citation():
    print("Testing inline citations")
    unique_id = "TestID"
    software_name = "CiteSoft"
    import_cite(unique_id, software_name)

def test_semantic_version():
    print("Testing semantic version comparison")
    unique_id = "semantic_ver_test"
    software_name = "CiteSoft"
    for _ in range(1, 4):
        kwargs = {"version": str(randint(0,10)) + '.' + str(randint(0,10)) + '.' + str(randint(0,10))}
        print("Adding citation with version : " + kwargs["version"])
        import_cite(unique_id, software_name, **kwargs)

def test_decimal_version():
    print("Testing decimal version comparison")
    unique_id = "decimal_ver_test"
    software_name = "CiteSoft"
    for _ in range(1, 4):
        kwargs = {"version": str(randint(0,10)) + '.' + str(randint(0,10))}
        print("Adding citation with version : " + kwargs["version"])
        import_cite(unique_id, software_name, **kwargs)

def test_wrapper_func():
    print("Testing wrapper function")
    a = 5
    b = 12
    print("Adding %d and %d", a, b)
    res = func_cite_test_add(a, b)
    print("Result : %d", res)

unique_id = "func_cite_test_add"
software_name = "CiteSoft"
kwargs = {"version": "1.1.5", "author": "CPH", "language": "Python"}
@module_call_cite(unique_id, software_name, **kwargs)
def func_cite_test_add(x, y):
    return x + y


if __name__ == '__main__':
    main()
