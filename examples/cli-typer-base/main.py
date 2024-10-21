from rich.console import Console
from rich.progress import track
from rich.style import errors as rich_style_errors
from services.api_consumer import Exchange
from services.calculator import Calculator, CalculatorLogger
from services.input_wrapper import InputWrapper
from tables.exchange import exchange_table_gen
from typer import Typer

app = Typer()


@app.command()
def hello(name: str, color: str = "yellow"):
    """Returns hello + the given name with rich color styling"""
    console = Console()
    try:
        console.print(f"Hello {name}", style=f"bold {color.lower()}")
    except rich_style_errors.MissingStyle:
        console.print(f"Hello {name}")
        console.print(f"Invalid color: {color}", style="bold red")


@app.command()
def currencies(euro: bool = True, official: bool = True):
    """Retrieves the values from an api
    https://bluelytics.com.ar/#!/api and render the data in a table using rich.
    """
    exchange = None
    for i in track(range(3), description="Fetching..."):
        exchange = Exchange()
    options = (euro, official)

    match options:
        case (True, False):
            del exchange.data["oficial"]
            del exchange.data["oficial_euro"]
        case (False, True):
            del exchange.data["oficial_euro"]
            del exchange.data["blue_euro"]
        case (False, False):
            del exchange.data["oficial"]
            del exchange.data["oficial_euro"]
            del exchange.data["blue_euro"]

    table = exchange_table_gen(exchange.data)
    console = Console()
    console.print(
        ":heavy_check_mark: :thumbs_up: :tada: :100: Last update:",
        exchange.data["last_update"][:-6],
    )
    console.print(table)


@app.command()
def conversion(json_response: bool = False) -> None:
    """Converts USD and EURO (official and blue) from ARS and to ARS"""
    console = Console()

    try:
        exchange = Exchange()
        console.print("Updated :heavy_check_mark:", style="bold blue")
    except Exception as e:
        console.print_exception()
        raise e
    if json_response:
        console.print_json(exchange.json_data.content.decode("utf8"))

    input = InputWrapper(exchange, console)

    calculator = Calculator(input.wrap())
    calculator.convert()
    CalculatorLogger(calculator)


if __name__ == "__main__":
    app()
