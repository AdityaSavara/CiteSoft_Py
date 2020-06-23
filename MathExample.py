import sys
import math
import CiteSoft
from CiteSoft import module_call_cite

software_name = "MathLib Example"
version = "1.0.0"

unique_id = "func_add"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def add(num1, num2):
    return num1 + num2

unique_id = "func_sub"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def subtract(num1, num2):
    return num1 - num2

unique_id = "func_mul"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def multiply(num1, num2):
    return num1 * num2

unique_id = "func_div"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def divide(num1, num2):
    return num1 / num2

unique_id = "func_mean"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def mean(list_of_num):
    result = 0
    for num in list_of_num:
        result = add(result, num)
    result = divide(result, len(list_of_num))
    return result

unique_id = "func_sqrt"
kwargs = {"version": "3.7.0", "author": "Python math lib devs"}
@module_call_cite(unique_id, software_name, **kwargs)
def sqrt(num):
    return math.sqrt(num)

unique_id = "func_sqr"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def sqr(num):
    return multiply(num, num)

unique_id = "func_var"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def sample_variance(list_of_num):
    meanVal = mean(list_of_num)
    result = 0
    for num in list_of_num:
        result = add(result, sqr(subtract(num, meanVal)))
    result = divide(result, (len(list_of_num) - 1))
    return result

unique_id = "func_stdev"
kwargs = {"version": version, "author": "CPH"}
@module_call_cite(unique_id, software_name, **kwargs)
def std_dev(list_of_num):
    return sqrt(sample_variance(list_of_num))

def export_citation(filepath=""):
    if filepath is not "":
        CiteSoft.compile_cite_software_log(filepath)
    else:
        CiteSoft.compile_cite_software_log()
