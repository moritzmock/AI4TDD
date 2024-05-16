import os
from dotenv import load_dotenv
from DeveloperAIHandler import DeveloperAIHandler, TEST_PASSED, TEST_FAILED, TEST_PASSED_WITHOUT_AI

load_dotenv('../.env')
import argparse
import sys

sys.path.append("../")
from utils import how_many_to_skip, str2bool


class Runner():

    def __init__(self, full_context, print_context, print_message, max_number_repetitions, file, generic_prompt):

        # Use variables
        openAI_key = os.getenv('OPEN_AI_KEY')
        self.handler = DeveloperAIHandler(
            openAI_key,
            "You are part of a Test Driven Development team. Your role is the development of code such that the provided code is fulfilled.",
            full_context,  # send always the full context
            print_context,  # print the context
            print_message,  # print the message from OpenAI
            file,  # file to the test case
            generic_prompt
        )
        self.max_number_repetitions = max_number_repetitions
        self.skip = how_many_to_skip(file)

    def run(self):
        self.handler.execute_tests(None)
        counter = self.skip
        while counter < (self.max_number_repetitions + self.skip):
            counter += 1
            result = self.handler.send_message(counter)
            if result == TEST_PASSED_WITHOUT_AI:
                print("The test case is already fulfilled, the code was not modified by ChatGPT.")
                counter = self.max_number_repetitions + self.skip
            else:
                result = self.handler.execute_new_test(counter)

                if result == TEST_PASSED:
                    print("Test case passed! You can inspect the updated code now!")
                    counter = self.max_number_repetitions + self.skip
                if result == TEST_FAILED:
                    print("Test failed! Resending it to ChatGPT...")





def params():
    parser = argparse.ArgumentParser(description='Description of your program.')

    # Add arguments
    parser.add_argument('--full_context', type=str2bool, help='sending the full context to OpenAI.', default=False)
    parser.add_argument('--print_context', type=str2bool, help='Printing the context before the it is send.',
                        default=False)
    parser.add_argument('--print_message', type=str2bool, help='Printing the message received from OpenAI.',
                        default=False)
    parser.add_argument('--max_number_repetitions', type=int,
                        help='Maximum number of chances given to OpenAI for solving a test case.', default=5)
    parser.add_argument('--file', type=str, help='Path to the file for the test case.', required=True)
    parser.add_argument('--generic_prompt', type=str, help='Prompt which is passed to the AI together with the error trace, production code, and test code.', default="I have the above test, what would be a minimal code so that the test no longer fails. Built-in functions are not allowed.")

    # Parse the command-line arguments
    return parser.parse_args()


if __name__ == '__main__':
    parser = params()

    runner = Runner(
        parser.full_context,
        parser.print_context,
        parser.print_message,
        parser.max_number_repetitions,
        parser.file,
        parser.generic_prompt
    )

    runner.run()
