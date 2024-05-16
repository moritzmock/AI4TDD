from openai import OpenAI
import subprocess
import sys
sys.path.append("..")
from utils import reshuffle_code

TEST_PASSED = "TEST_PASSED"
TEST_FAILED = "TEST_FAILED"
TEST_PASSED_WITHOUT_AI = "TEST_PASSED_WITHOUT_AI"


def get_path(filename, idx, filetype="py"):
    return "{}.{}".format(filename.replace(".py", "")+"_"+str(idx), filetype)


def get_next_filename(filename, idx):
    return filename + "_" + str(idx)


class DeveloperAIHandler:
    def __init__(self, key, role, full_context, print_context, print_message, file, generic_prompt):
        self.client = OpenAI(api_key=key)
        self.role = role
        self.messages_send = []
        self.messages_received = []
        self.messages_received_parsed_code = []
        self.errors = []
        self.current_test_file = file
        self.full_context = full_context
        self.print_context = print_context
        self.print_message = print_message
        self.generic_prompt = generic_prompt

    def get_next_message(self, idx):
        trace = self.get_traces_of_last_run()
        if trace == TEST_PASSED:
            return TEST_PASSED
        test_and_trace = trace + "\n" + self.get_tests(idx)

        return test_and_trace + "\n\n" + self.generic_prompt

    def save_context(self, context, idx_file):
        filename = self.current_test_file

        text2save = ""
        for idx in range(len(context)):
            element = context[idx]
            text2save = text2save + "role - " + element["role"] + "\n"
            text2save = text2save + "content:\n"
            #print(element["content"])
            content = element["content"].split("\n")
            for index in range(len(content)):
                line = content[index]
                text2save = text2save + line + "\n"

            text2save = text2save + "\n\n=================================================\n\n"

        path = get_path(filename, idx_file, "txt").replace(".txt", "_context_developer.txt")

        with open(path, 'w') as file:
            file.write(text2save)



    def create_context(self):
        context = [{"role": "system", "content": self.role}]
        for idx in range(len(self.messages_send)):
            context.append({"role": "user", "content": self.messages_send[idx]})
            context.append({"role": "assistant", "content": self.messages_received[idx]})

        return context

    def send_message(self, idx):
        context = self.create_context()
        next_message = self.get_next_message(idx)
        if next_message == TEST_PASSED:
            return TEST_PASSED_WITHOUT_AI
        context.append({"role": "user", "content": next_message})

        if not self.full_context:
            context = [
                   {"role": "system", "content": self.role},
                   {"role": "user", "content": next_message}
               ]

        self.save_context(context, idx)

        if self.print_context:
            print("------ CONTEXT START -------")
            print(context)
            print("------ CONTEXT END -------")

        response = self.client.chat.completions.create(
           model="gpt-3.5-turbo-16k",
           messages=context
        )
        #response = "To make the test pass without any errors, we need to define the `TextFormatter` class. Here's a minimal code that defines the `TextFormatter` class:\n" \
        #           "\n" \
        #           "```python\n" \
        #           "class TextFormatter:\n" \
        #           "    pass\n" \
        #           "```\n" \
        #           "\n" \
        #           "Now, the test should pass without any errors."

        self.messages_send.append(next_message)
        message = response.choices[0].message.content  # TODO remove comment
        #message = response

        path = get_path(self.current_test_file, idx, "txt").replace(".txt", "_response_developer.txt")
        file_opener = open(path, 'w')
        file_opener.writelines(message)
        file_opener.close()

        self.messages_received.append(message)
        self.messages_received_parsed_code.append(self._parse_message(message))

    def execute_new_test(self, idx):
        self.merge_files(idx)
        self.execute_tests(idx)
        if self.errors[-1] == TEST_PASSED:
            self.merge_files(idx, update_original_file=True)
            return TEST_PASSED
        return TEST_FAILED

    def get_tests_without_previous_code(self, idx):
        old_code = self.get_tests(idx).split("\n")
        for idx in range(len(old_code)):
            line = old_code[idx]
            if line.startswith("import unittest"):
                return "\n".join(old_code[idx:])

        return "\n".join(old_code)

    def get_code_without_test_case(self):
        code = self.messages_received_parsed_code[-1].split("\n")

        for idx in range(len(code)):
            line = code[idx]
            if line.startswith("import unittest"):
                return "\n".join(code[:idx])
        return "\n".join(code)

    def merge_files(self, idx, update_original_file=False):
        code = self.get_code_without_test_case()
        test_cases = self.get_tests_without_previous_code(idx)
        # print(code)
        # print(test_cases)
        # print("hier")
        complete_code = code + "\n\n" + test_cases

        if update_original_file:
            file_opener = open(self.current_test_file, 'w')
            file_opener.writelines(reshuffle_code(complete_code))
            file_opener.close()

        if not update_original_file:
            path = get_path(self.current_test_file, idx)
            file_opener = open(path, 'w')
            file_opener.writelines(reshuffle_code(complete_code))
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
        # print(code)

        if len(result) == 0:
            return message
        return "\n".join(result)

    def execute_tests(self, idx):
        path = get_path(self.current_test_file, idx)
        result_sub_process = subprocess.run(["python", path if idx is not None else self.current_test_file], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, universal_newlines=True)
        if "OK" not in result_sub_process.stderr.split("\n")[-2]:
            self.errors.append([result_sub_process.stderr])
        else:
            self.errors.append(TEST_PASSED)

    def get_traces_of_last_run(self):
        if self.errors[-1] == TEST_PASSED:
            return TEST_PASSED
        return "\n".join(self.errors[-1])

    def get_tests(self, idx):
        file = open(self.current_test_file, 'r')
        lines = file.readlines()
        return "".join(lines)
