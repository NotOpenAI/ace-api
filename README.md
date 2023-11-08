# Prerequisites

Make sure **Python3** is available on your machine. This project is using version 3.11. If you have multiple versions of Python, you can use a Python version manager such as [pyenv](https://github.com/pyenv/pyenv).

# Development

The following steps outline additional setups to work on this project.

## Install Dependencies
Make sure you have [pipx](https://pypa.github.io/pipx/) installed (requires pip 19.0+).

You can verify it by running:
```
pipx --version
```

Then install [poethepoet](https://poethepoet.natn.io/index.html) and [poetry](https://python-poetry.org/docs/master/) by running:
```
pipx install poethepoet && pipx install poetry
```
Finally, go to your root directory and run:

```
poe i
```
to install the dependencies and pre-commit hooks. You only have to run this once unless new packages have been added.

## Connect to Database
Create a **.env** file in the root directory and enter the credentials in the same format as **.env.example**

## Start Development Server

Navigate to the root directory and run:
```
poe start
```
to see live changes. This will start the application at `localhost:8000`
