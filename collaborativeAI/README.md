### ChatGPT4TDD

The actor writes a test case, after which the following command is executed to send it ChatGPT
```cmd
python runner.py --file <filepath> --generic_prompt 'I have the above test, what would be a minimal code so that the test no
longer fails. Built-in functions are not allowed.'
```
