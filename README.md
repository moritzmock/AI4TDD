# AI4TDD

This repository contains the replication package for the paper *Generative AI for Test Driven Development: preliminary results*. The work was conducted by Moritz Mock, Jorge Melegati, and Barbara Russo.

Link to preprint: [doi.org/10.48550/arXiv.2405.10849](https://doi.org/10.48550/arXiv.2405.10849)

Link to publication (open access): [https://doi.org/10.1007/978-3-031-72781-8_3](https://doi.org/10.1007/978-3-031-72781-8_3)

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

## How to cite

#### Preprint

```bibtex
@misc{mock2024generative,
      title={Generative AI for Test Driven Development: Preliminary Results}, 
      author={Moritz Mock and Jorge Melegati and Barbara Russo},
      year={2024},
      eprint={2405.10849},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      doi={10.48550/arXiv.2405.10849}
}
```
#### Publication
```bibtex
@InProceedings{10.1007/978-3-031-72781-8_3,
      author="Mock, Moritz
      and Melegati, Jorge
      and Russo, Barbara",
      editor="Marchesi, Lodovica
      and Goldman, Alfredo
      and Lunesu, Maria Ilaria
      and Przyby{\l}ek, Adam
      and Aguiar, Ademar
      and Morgan, Lorraine
      and Wang, Xiaofeng
      and Pinna, Andrea",
      title="Generative AI for Test Driven Development: Preliminary Results",
      booktitle="Agile Processes in Software Engineering and Extreme Programming -- Workshops",
      year="2025",
      publisher="Springer Nature Switzerland",
      address="Cham",
      pages="24--32",
      abstract="Test Driven Development (TDD) is one of the major practices of Extreme Programming for which incremental testing and refactoring trigger the code development. TDD has limited adoption in the industry, as it requires more code to be developed and experienced developers. Generative AI (GenAI) may reduce the extra effort imposed by TDD. In this work, we introduce an approach to automatize TDD by embracing GenAI either in a collaborative interaction pattern in which developers create tests and supervise the AI generation during each iteration or a fully-automated pattern in which developers only supervise the AI generation at the end of the iterations. We run an exploratory experiment with ChatGPT in which the interaction patterns are compared with the non-AI TDD regarding test and code quality and development speed. Overall, we found that, for our experiment and settings, GenAI can be efficiently used in TDD, but it requires supervision of the quality of the produced code. In some cases, it can even mislead non-expert developers and propose solutions just for the sake of the query.",
      isbn="978-3-031-72781-8"
}
```

