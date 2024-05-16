import os
import re
import fnmatch
import argparse


def how_many_to_skip(original_file, multiplier=2):
    file_split = original_file.split("/")
    path = "/".join(file_split[0:len(file_split) - 1])
    path = "." if path == "" else path
    original_file = file_split[-1]
    files = os.listdir(path)
    search_file = original_file.replace(".py", "") + "_*.py"
    matching_files = [file for file in files if fnmatch.fnmatch(file, search_file)and len(file.replace(original_file.replace(".py", ""), "").split("_")) == multiplier +1]
    pattern = re.compile(r'\d+')

    # Extract numbers from each filename and create an array
    numbers_array = [int(pattern.search(file).group()) for file in matching_files if pattern.search(file)]

    files_to_skip = max(numbers_array) if len(numbers_array) > 0 else 0

    return files_to_skip


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def read_file(path):
    # Open the file in read mode
    if os.path.exists(path):
        with open(path, 'r') as file:
            # Read the contents of the file
            contents = file.read()
            # Print the contents
            return contents

def reshuffle_code(code, path=None):
    classes = extract_classes(code)

    result = []
    productionCode = list(filter(lambda x: x["testCase"] == False, classes))
    testCases = list(filter(lambda x: x["testCase"] == True, classes))

    if len(productionCode) == 0 and path is not None:
        old_code = read_file(path)
        if old_code is not None:
            classes_old = extract_classes(old_code)
            productionCode = list(filter(lambda x: x["testCase"] == False, classes_old))

    [result.append(element["class"]) for element in productionCode]
    result.append("import unittest\n")
    [result.append(element["class"]) for element in testCases]

    return "\n\n".join(result)


def extract_classes(code):
    code_split = code.split("\n")
    result = []
    startLine = None
    tentative_result_of_one_class = []
    # removes import unittest from the code, regardless where it is
    for idx in range(len(code_split)):
        line = code_split[idx]
        if not line.startswith("import unittest"):
            result.append(line)

    code_split = result
    result = []
    for idx in range(len(code_split)):
        line = code_split[idx]
        if ((line.startswith("class") or line.startswith("def")) or idx == len(
                code_split) - 1) and startLine is not None:
            if idx == len(code_split) - 1:
                tentative_result_of_one_class.append(line)
            result.append({
                "startLine": startLine,
                "endLine": idx,
                "class": "\n".join(tentative_result_of_one_class),
                "testCase": True if "unittest.TestCase" in tentative_result_of_one_class[0] else False
            })
            tentative_result_of_one_class = []
            startLine = None
        if (line.startswith("class") or line.startswith("def")) and startLine is None:
            startLine = idx
        if startLine is not None:
            tentative_result_of_one_class.append(line)

    return result
