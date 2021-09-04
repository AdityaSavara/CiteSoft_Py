import sys
import math
try:
    import CiteSoft
except:
    import os #The below lines are to allow CiteSoftLocal to be called regardless of user's working directory.
    lenOfFileName = len(os.path.basename(__file__)) #This is the name of **this** file.
    absPathWithoutFileName = os.path.abspath(__file__)[0:-1*lenOfFileName]
    sys.path.append(absPathWithoutFileName)
    import CiteSoftLocal as CiteSoft

#Here CiteSoft is used with an example module called "MathExample"
#Note that the unique_id should be something truly unique (no other software would use it).
#Typically, unique_id is a DOI or a URL.
#The author field is typically a list object with names as strings, but can also just be a single string.
#Note that there is a function called sqrt which uses the python math module, and uses a *different* citation.

software_name = "CiteSoft Math Example"
version = "1.0.0"
MathExample_unique_id = "https://github.com/AdityaSavara/CiteSoft_py/blob/master/MathExample.py"
kwargs = {"version": version, "author": ["Aditya Savara", "CPH"]} 

#The below line will cause this module's citation to be exported any time the module is imported. 
#The 'write_immediately = True' causes the checkpoint to be written at the time of export rather than stored.
CiteSoft.import_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", write_immediately=True, **kwargs)

@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)
def add(num1, num2):
    return num1 + num2

@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)
def subtract(num1, num2):
    return num1 - num2

@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)
def multiply(num1, num2):
    return num1 * num2

@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)
def divide(num1, num2):
    return num1 / num2

@CiteSoft.after_call_compile_consolidated_log() #This will cause the consolidated log to be complied after the mean function is called. #note that we put it after the module_call_cite so that it is a wrapper around that wrapper and occurs second.
@CiteSoft.module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)
def mean(list_of_num):
    result = 0
    for num in list_of_num:
        result = add(result, num)
    result = divide(result, len(list_of_num))
    return result

math_unique_id = "https://docs.python.org/3/library/math.html"
math_software_name = "The Python Library Reference: Mathematical functions"
math_version = str(sys.version).split("|")[0] #This is the python version.
math_kwargs = {"version": math_version, "author": "Van Rossum, Guido", "cite": "Van Rossum, G. (2020). The Python Library Reference, release 3.8.2. Python Software Foundation."}
@CiteSoft.module_call_cite(unique_id=math_unique_id, software_name=math_software_name, **math_kwargs)
def sqrt(num):
    return math.sqrt(num)

@CiteSoft.module_call_cite(MathExample_unique_id, software_name, **kwargs)
def sqr(num):
    return multiply(num, num)

@CiteSoft.module_call_cite(MathExample_unique_id, software_name, **kwargs)
def sample_variance(list_of_num):
    meanVal = mean(list_of_num)
    result = 0
    for num in list_of_num:
        result = add(result, sqr(subtract(num, meanVal)))
    result = divide(result, (len(list_of_num) - 1))
    return result

@CiteSoft.module_call_cite(MathExample_unique_id, software_name, **kwargs)
def std_dev(list_of_num):
    return sqrt(sample_variance(list_of_num))

@CiteSoft.after_call_compile_consolidated_log() #This will cause the consolidated log to be complied after the mean function is called. #note that we put it after the module_call_cite so that it is a wrapper around that wrapper and occurs second.
@CiteSoft.module_call_cite(MathExample_unique_id, software_name, **kwargs)
def cite_me(): #This is just an example of how a package creating dev-user could make a function that other dev-users relying on their package could call at the very end of doing everything, so that no calls to CiteSoft would need to occur during runtime.
    pass

#note that the above lines of code simply add to the file CiteSoftwareCheckPoints
#if one wants to create a consolidated log that removes duplicates, one can call a CiteSoft function
#This is considered appropriate to do at the end of a complicated program, but is not necessary.
#it would have been possible to also use decorators on any of the above functions, like @CiteSoft.after_call_compile_checkpoints_log or @CiteSoft.after_call_compile_consolidated_log.  Note that chained/stacked decorators are performed in "first in last out" order, since they are wrappers on wrappers. So if a function has both @CiteSoft.module_call_cite and @after_call_compile_consolidated_log, the @CiteSoft.module_call_cite should be second.
def export_citation_checkpoints(filepath=""):
    if filepath is not "":
        CiteSoft.compile_checkpoints_log(filepath)
    else:
        CiteSoft.compile_checkpoints_log()
