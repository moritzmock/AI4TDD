# GenerativeAI4TDD

### Installation

```
python -m venv env

source env/bin/activate //for macOS and Linux
env\Scripts\activate // for Windows

pip install -r requirements.txt
```

### Setup

Creating a file `.env` in the project's root containing an API key for OpenAI is mandatory.

```
OPEN_AI_KEY=<our_key>
```

For more details, please follow the instructions under this link [https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key)


### Experiments

In the folder [collaborativeAI](collaborativeAI), the implementation of the code for the collaborativeAI approach, which was used to conduct the experiments with participants, can be found.

In the folder [full-automatedTDD](fully-automatedTDD), the implementation for the full automation of TDD using the AI can be found.

Both folders contain instructions on how to run the programs.


### Obtained results

All the collected data can be found in the folder [experiments](experiments).
