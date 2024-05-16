import argparse
import os
import sys
sys.path.append("..")
from TestCaseAIHandler import TestCaseAIHandler
from dotenv import load_dotenv
from utils import str2bool

load_dotenv('../.env')



CREATE_TEST_CASE = "CREATE_TEST_CASE"
CREATE_CODE = "CREATE_CODE"
INTERACTIVE = "INTERACTIVE"

class Runner():

    def __init__(self, text, command, print_message, pass_file, folder, generic_production_code_prompt_enhancement, incorrect_test_cases_created=0):
        openAI_key = os.getenv('OPEN_AI_KEY')
        self.handler = TestCaseAIHandler(
            openAI_key,
            "You are part of a Test Driven Development team. Your role is the tester, create out of a textual description a test case using the library 'unittest'.",
            text,
            print_message,
            pass_file,
            folder,
            generic_production_code_prompt_enhancement,
            incorrect_test_cases_created
        )
        self.command = command
        self.text = text

    def run(self):
        if self.command == CREATE_TEST_CASE:
            if self.text == None:
                print("Parameter for --text is not provided, but mandatory! \nExiting...")
                quit(-1)
            self.handler.create_test_case()
        if self.command == CREATE_CODE:
            self.handler.create_code()



def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--prompt", type=str, required=False)
    parser.add_argument("--command", type=str, required=True, choices=[CREATE_CODE, CREATE_TEST_CASE, INTERACTIVE])
    parser.add_argument("--print_message", type=str2bool, required=False, default=False)
    parser.add_argument("--pass_file", type=str, required=False)
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--generic_production_code_prompt_enhancement", type=str, default="Write the next line of the production code")

    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parser()
    prompt = 'Use the Assertion First pattern in TDD and stub and drivers to develop the first barely minimal test and production code for the feature “{}" with {}. Do not provide a solution for other input classes'

    if args.command == INTERACTIVE:
        print('The first step is to create the first test.\n')
        incorrect_test_cases_created = 0 # workaround for issues with the test case should be redone
        while True:
            feature = input('What is the feature description?\n')
            values = input('What is/are the parameter(s) description? (e.g. width=10 and word="word")\n')

            runner = Runner(prompt.format(feature, values), CREATE_TEST_CASE, args.print_message, args.pass_file, args.folder, args.generic_production_code_prompt_enhancement, incorrect_test_cases_created)
            runner.run()

            print('Please, check the generated test case.\n')
            incorrect_test_cases_created = incorrect_test_cases_created + 1

            while True:
                test_message = 'Generate a new ' if incorrect_test_cases_created == 0 else 'Recreate'
                next_step = input('What would you like to do next? ' + test_message + ' [T]est case, create [C]ode, or [E]nd?\n'+
                                  'Please type the corresponding letter: ')
                if next_step.upper() == 'T':
                    break
                elif next_step.upper() == 'C':
                    prompt = prompt.replace("Use", "Keep the existing tests and add one by using")
                    incorrect_test_cases_created = 0
                    runner = Runner("", CREATE_CODE, args.print_message, None, args.folder, args.generic_production_code_prompt_enhancement)
                    runner.run()
                    print('Please, check the generated code.\n')
                elif next_step.upper() == 'E':
                    confirm_end = input('Are you sure you want to close the exercise? [Y/N]:')
                    if confirm_end.upper() == 'Y':
                        quit()
                else:
                    print('Unrecognized letter.\n')
    else:
        runner = Runner(
            args.prompt,
            args.command,
            args.print_message,
            args.pass_file,
            args.folder,
            args.generic_production_code_prompt_enhancement
        )

    runner.run()
