from openai import OpenAI
import subprocess
import sys
import os
from utils import how_many_to_skip, \
    reshuffle_code

sys.path.append("..")


TEST_PASSED = "TEST_PASSED"


# Format of the test cases is
# test_case_*.py


def create_folder_if_needed(folder_name):
    # Check if the folder already exists
    if not os.path.exists(folder_name):
        try:
            # Create the folder
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created successfully.")
        except OSError as e:
            print(f"Error creating folder '{folder_name}': {e}")
    else:
        print(f"Folder '{folder_name}' already exists.")


class TestCaseAIHandler():

    def __init__(self, key, role, text, print_message, pass_file, folder, generic_production_code_prompt,
                 incorrect_test_cases_created):
        self.client = OpenAI(api_key=key)
        self.role = role
        self.text = text
        self.print_message = print_message
        self.messages_sent = []
        self.messages_received = []
        self.messages_received_parsed_code = []
        self.errors = []
        self.pass_file = pass_file
        create_folder_if_needed(folder)
        self.folder = folder if folder is not None else '.'
        self.incorrect_test_cases_created = incorrect_test_cases_created
        self.generic_production_code_prompt = generic_production_code_prompt

    def get_last_test_case_number(self):
        return how_many_to_skip("{}/test_case.py".format(self.folder), multiplier=1)

    def get_last_test_case_path(self):
        number = self.get_last_test_case_number() - self.incorrect_test_cases_created
        return "test_case_" + str(number) + ".py"

    def get_base_filename_for_context(self):
        number = self.get_last_test_case_number()
        base_filename = "test_case_" + str(number + 1)
        return base_filename

    def get_filename_for_context(self):
        base_filename = self.get_base_filename_for_context()
        return base_filename + "_context_tester.txt"

    def create_context(self):
        context = [{"role": "system", "content": self.role}]

        return context

    def get_previous_code(self):
        with open(self.pass_file, 'r') as file:
            # Read the entire contents of the file into a string
            content = file.read()

        return content

    def get_next_message(self):

        number = self.get_last_test_case_number()
        if self.pass_file is None:
            number = number - self.incorrect_test_cases_created
            self.pass_file = self.folder + '/' + self.get_last_test_case_path() if number > 0 else None
        previous_code = "" if self.pass_file is None else "Given the below existent code:\n" + self.get_previous_code()

        return {"role": "user",
                "content": previous_code + "\nGiven the following textual description of the test case, provide a minimal test case:\n" + self.text + "\n\nAssume that the class will be written in the same file!"}

    def save_context(self, context):
        filename = self.folder + "/" + self.get_filename_for_context()

        text2save = ""
        for idx in range(len(context)):
            element = context[idx]
            text2save = text2save + "role - " + element["role"] + "\n"
            text2save = text2save + "content:\n"
            content = element["content"].split("\n")
            for index in range(len(content)):
                line = content[index]
                text2save = text2save + line + "\n"

            text2save = text2save + "\n\n=================================================\n\n"
        with open(filename, 'w') as file:
            file.write(text2save)

    def clean_code(self):
        code = self.messages_received_parsed_code[-1][0].split("\n")
        result = []
        for idx in range(len(code)):
            line = code[idx]
            if not line.startswith("from"):
                result.append(line)

        return "\n".join(result)


    def create_test_case(self):
        context = self.create_context()
        next_message = self.get_next_message()
        context.append(next_message)

        self.save_context(context)

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=context
        )

        self.messages_sent.append(next_message)
        message = response.choices[0].message.content  # TODO remove comment
        # message = response
        self.messages_received.append(message)
        self.messages_received_parsed_code.append(self._parse_message(message))
        
        path = self.folder + "/" + self.get_base_filename_for_context() + "_response_tester.txt"
        self.save_to_file(message, path)

        code = self.clean_code()
        path = self.folder + "/" + self.get_base_filename_for_context() + ".py"

        self.save_to_file(reshuffle_code(code, self.folder + "/" + self.get_last_test_case_path()), path)

        print("Generated test case is stored in file: " + path)

    def save_to_file(self, message, path):
        file_opener = open(path, 'w')
        file_opener.writelines(message)
        file_opener.close()

    def _parse_message(self, message):
        if self.print_message:
            print("------ start message")
            print(message)
            print("------   end message")

        split_message = message.split("\n")

        code = False
        result = []
        tmp = []
        for line in split_message:
            if line.startswith("```") and len(tmp) != 0:
                result.append("\n".join(tmp))
                tmp = []
                break

            if code:
                tmp.append(line)

            if line.startswith("```"):
                code = True
                tmp = []

        if len(result) == 0:
            return [message]

        return result

    def create_code(self):
        path = self.folder + "/" + self.get_last_test_case_path()

        result_sub_process = subprocess.run(["python", "../collaborativeAI/runner.py", "--file", path, "--generic_prompt",
                                             self.generic_production_code_prompt],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, universal_newlines=True)

        print("Return value from generating code!")
        print("out")
        print(result_sub_process.stdout)
        print("err")
        print(result_sub_process.stderr)
