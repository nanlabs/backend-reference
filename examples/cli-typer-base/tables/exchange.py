from rich.style import Style
from rich.table import Table


def exchange_table_add_rows(data: dict, table: Table) -> Table:
    for key, value in data.items():

        if key == "last_update":
            continue
        table.add_row(
            key.upper(),
            "AR$ " + str(value["value_buy"]),
            "AR$ " + str(value["value_sell"]),
            end_section=True
        )
    return table


def exchange_table_gen(data: dict) -> Table:
    table = Table()
    table.add_column(
        "CURRENCY",
        justify="center",
        width=30,
        header_style=Style(color="green", bold=True),
        style=Style(
            color="green",
            bold=True
        )
    )
    table.add_column(
        "Buy price",
        justify="center",
        width=15,
        header_style=Style(color="red", bold=True),
        style=Style(
            bgcolor="white",
            color="Red"
        )
    )
    table.add_column(
        "Sell price",
        justify="center",
        width=15,
        header_style=Style(color="blue", bold=True),
        style=Style(
            bgcolor="white",
            blink=True,
            color="blue"
        )
    )
    return exchange_table_add_rows(data, table)
