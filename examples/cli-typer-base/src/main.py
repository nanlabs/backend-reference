from rich.console import Console
from rich.progress import track
from services.api_consumer import Exchange
from tables.exchange import exchange_table_gen
from typer import Typer

app = Typer()


@app.command()
def dollar():
    """This command retrieves the values from an api
    https://bluelytics.com.ar/#!/api
    """
    exchange = None
    for i in track(range(3), description="Fetching..."):
        exchange = Exchange()

    table = exchange_table_gen(exchange.data)
    console = Console()
    console.print(
        ":heavy_check_mark: :thumbs_up: :tada: :100: Last update: " +
        exchange.data["last_update"][:-6]
    )
    console.print(table)


if __name__ == '__main__':
    app()
