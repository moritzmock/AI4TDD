# AI4TDD

This repository contains the replication package for the paper *Generative AI for Test Driven Development: preliminary results*. The work was conducted by Moritz Mock, Jorge Melegati, and Barbara Russo.

## Abstract

Test Driven Development (TDD) is one of the major practices of Extreme Programming for which incremental testing and refactoring trigger the code development. TDD has limited adoption in the industry, as it requires more code to be developed and experienced developers. Generative AI may reduce the extra effort imposed by TDD. In this work, we introduce an approach to automatize TDD by embracing generative AI either in a collaborative interaction pattern in which developers create tests and supervise the AI generation during each iteration or a fully automated pattern in which developers only supervise the AI generation at the end of the iterations. We run an exploratory experiment with ChatGPT in which the interaction patterns are compared with the non-AI TDD for test, code quality, and development speed. Overall, we found that, for our experiment and settings, generative AI can be efficiently used in TDD, but it requires supervision of the quality of the code produced. In some cases, it can even mislead non-expert developers and propose solutions just for the sake of the query.

## Installation

```
python -m venv env

source env/bin/activate //for macOS and Linux
env\Scripts\activate // for Windows

pip install -r requirements.txt
```

## Setup

Creating a file `.env` in the project's root containing an API key for OpenAI is mandatory.

```
OPEN_AI_KEY=<our_key>
```

For more details, please follow the instructions under this link [https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key)


## Experiments

In the folder [collaborativeAI](collaborativeAI), the implementation of the code for the collaborativeAI approach, which was used to conduct the experiments with participants, can be found.

In the folder [full-automatedTDD](fully-automatedTDD), the implementation for the full automation of TDD using the AI can be found.

Both folders contain instructions on how to run the programs.


## Obtained results

All the collected data can be found in the folder [experiments](experiments).
