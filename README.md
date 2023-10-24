# Prerequisites

Make sure **Python3** is available on your machine. This project is using version 3.11

# Development

The following steps outline additional setups to work on this project.

## Install Dependencies

Go to your root directory and run:

```
pip3 install -r requirements.txt
```

## Start Development Server

Navigate to the `src` directory and run:
```
uvicorn main:app --reload
```
to see live changes. This will start the application at `localhost:8000`

# Pre-commit
Make sure your run the Python formatter frm the root directory before committing:
```
black .
```