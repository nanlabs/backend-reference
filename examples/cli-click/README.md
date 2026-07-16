# CLI Base with Click

## Overview

This is a simple CLI example using [Click](https://click.palletsprojects.com/), comparable to the Typer CLI example. It demonstrates how to create a basic command-line interface with help (`-h`, `--help`) and version (`-v`, `--version`) support.

## Prerequisites

**Python 3.10** or higher

## Setup

You must step into the root of this example directory in your terminal:

```bash
cd examples/cli-click
```

1. Create a virtual env `python3 -m venv venv`.
2. Activate venv `source ./venv/bin/activate` (or `.\venv\Scripts\activate` on Windows).
3. Install dependencies `pip install -r requirements.txt`

## Run commands

### Help

```bash
python main.py -h
# or
python main.py --help
```

### Version

```bash
python main.py -v
# or
python main.py --version
```

### Hello

```bash
python main.py --name "World"
```

## Running Tests

To run the automated tests:

```bash
pytest test_main.py
```
