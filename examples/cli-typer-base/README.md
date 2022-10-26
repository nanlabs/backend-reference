# CLI Base with Typer + Rich

## Overview

In this example the idea was to provide simple implementations of [Typer](https://typer.tiangolo.com/) added to the power of [Rich](https://rich.readthedocs.io/en/stable/introduction.html) that allows you as developer to beatify the console output. It's important to take into account that these examples are written using Python 3.10 features

## Rich Features

- **Colors**:
  - 4-bit color
  - 8-bit color
  - Truecolor (16.7 million)
  - Dumb terminals
  - Automatic color conversion
- **Styles**:
  - All ansi styles: bold, dim, italic, underline, strikethrough, reverse, and even blink.
- **Text**
  - Word wrap text. Justify left, center, right or full.
- **Asian language support**
- **Markup**
  - Rich supports a simple bbcode-like markup for color, style, and emoji! 👍 🍎 🐜 🐻 🥖 🚌
- **Tables**
- **Syntax highlighting & pretty printing**
- **Markdown**: Supports much of the *markdown* syntax!
  - Headers
  - Basic formatting: **bold**, *italic*, `code`
  - Block quotes
  - Lists, and more...
- **Progress bars**
- **Columns**
- **styled logging handler**
- **Tracebacks**
- **Etc.**

---

## Prerequisites

**Python 3.10** or higher

---

## Setup

You must step into the root of example directory in your terminal

1. Create a virtual env `python3 -m venv .venv`.
2. Activate venv `source ./venv/bin/activate`
3. Install dependencies `pip install requirements.txt`
4. If you need to install dev dependencies simply run `pip install requirements_dev.txt`

---

## Run commands

First execute the **setup process** described in the previous section.
Once created the virtual environment and installed dependencies you can run commands. There are two ways, and both are valid:

```bash
python main.py <command>
```

or

```bash
python -m main <command>
```

---

### Help

```bash
python main.py --help
```

> This command shows the available commands with it's description, that is taken from the command docstring.

---

### Hello

```bash
python main.py hello <NAME> --color <COLOR>
```

> Returns hello + the given name with rich color styling. With this command you can specify the output color by adding the `--color` and specifying the desired color.
>
> E.G.
>
> `python main.py hello Joe --color red`

#### Hello Options

```bash
--color     TEXT      [default: yellow]
--help      Show the options and exit.
```

---

### Currencies

```bash
python main.py currencies
```

> Retrieves the values from [Bluelytic](https://bluelytics.com.ar/#!/api) and render the data in a table using rich.

#### Currencies Options

```bash
--euro      --no-euro          [default: euro]
--official  --no-official      [default: official]
--help      Show the options and exit.
```

---

### Exchange rate conversion

```bash
python main.py conversion
```

> Allows the user to convert from **ars** to **usd** or **euro** (blue and official) and from **usd** or **euro** (blue and official) to **ars** (not between dollar and euro) taking this into account:

As the API's response has 3 values for every currency (except ARS) buy, sell and average.

``` json
{
  "oficial": {
    "value_avg": 157.0,
    "value_sell": 161.0,
    "value_buy": 153.0
  },
  "blue": {
    "value_avg": 289.0,
    "value_sell": 291.0,
    "value_buy": 287.0
  },
  "oficial_euro": {
    "value_avg": 169.0,
    "value_sell": 173.0,
    "value_buy": 165.0
  },
  "blue_euro": {
    "value_avg": 311.0,
    "value_sell": 313.0,
    "value_buy": 309.0
  },
  "last_update": "2022-10-24T12:30:40.739232-03:00"
}
```

- If the conversion is from **ARS** to **USD** or **EURO** (official or blue) the sell value (the highest value) is used to calculate the exchange rate.
- If the conversion is from **USD** or **EURO** (official or blue) to **ARS** the buy value (the lowest value) is used to calculate the exchange rate.

#### Conversion Options

```bash
--json-response   --no-json-response       [default: --no-json-response]
--help            Show the options and exit.
```
