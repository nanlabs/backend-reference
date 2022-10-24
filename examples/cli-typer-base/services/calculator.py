from math import pow

from entities.currencies import Currency, OperationType
from rich.style import Style
from rich.table import Table
from services.input_wrapper import ConversionParams


class Calculator:
    def __init__(
        self,
        conversion_params: ConversionParams
    ) -> None:
        self.conversion_params = conversion_params

    def _get_exchange_value(self) -> None:
        match self.conversion_params.from_currency:
            case Currency.ARS.value:
                self.conversion_params.exchange = pow(
                    self.conversion_params.exchange
                    .get(self.conversion_params.to_currency)
                    .get(OperationType.SELL.value),
                    -1
                )
            case _:
                self.conversion_params.exchange = self.conversion_params.exchange \
                    .get(self.conversion_params.from_currency).get(OperationType.BUY.value)

    def convert(self) -> None:
        self._get_exchange_value()
        self.converted_value = self.conversion_params.amount * self.conversion_params.exchange


class CalculatorLogger:
    def __init__(self, calc: Calculator) -> None:
        self.calculator = calc
        self.logger()

    def logger(self) -> None:
        console = self.calculator.conversion_params.console

        table = Table()
        table.add_column(
            "FROM",
            justify="center",
            width=30,
            header_style=Style(color="blue", bold=True),
            style=Style(
                color="blue"
            )
        )
        table.add_column(
            "TO",
            justify="center",
            width=30,
            header_style=Style(color="green", bold=True),
            style=Style(
                color="green",
                bold=True
            )
        )

        table.add_row(
            self.calculator.conversion_params.from_currency.upper(),
            self.calculator.conversion_params.to_currency.upper(),

        )
        table.add_row(
            str(self.calculator.conversion_params.amount),
            str("%.2f" % self.calculator.converted_value)
        )

        console.print(table)
