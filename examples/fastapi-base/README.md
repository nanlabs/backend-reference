# FastApi base

## Prerequistes

- Python
  * Debian/Ubuntu
        ```bash
        apt install python3```
  * MacOS
        ```bash
        brew install python@3```
- Virtualenv

  ```bash
    pip3 install virtualenv```

## Install steps

1. Create virtualenv

  ```bash
    virtualenv -p python3 env```
2. Activate virtualenv
    ```bash
    source env/bin/activate```
3. Install the requirements from corresponding requirements file
    - For development
    ```bash
        pip install -r requirements.dev.txt
    ```
    - For production
    ```bash
        pip install -r requirements.txt
    ```

## Usage

- Start up application
    ```bash
    python src/main.py
    ```
- Open documentation
    ```bash
    # Follow the URL for OpenApi documentation
    http://0.0.0.0:8000/docs#/
    # you can try also with ReDoc documentation
    http://0.0.0.0:8000/redoc
    ```
