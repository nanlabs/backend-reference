from dataclasses import dataclass

from entities.currencies import CURRENCY_NAMES, Currency
from rich.console import Console
from services.api_consumer import Exchange


class InputValidation:

    @staticmethod
    def existence_name_validator(command: str) -> None:
        if command not in CURRENCY_NAMES:
            raise ValueError("Invalid value, please ty again")


@dataclass
class ConversionParams:
    exchange: dict
    console: Console
    amount: float
    from_currency: str
    to_currency: str


class InputWrapper:
    def __init__(self, exchange: Exchange, console: Console) -> None:
        self._exchange_data = exchange.data
        self._console = console
        self._amount = 0
        self._from_currency: Currency = None
        self._to_currency: Currency = None

    def _from_currency_input(self) -> None:
        self._console.print(CURRENCY_NAMES)
        self._console.print("Original currency", style="bold green")
        command = input("FROM: ").upper()
        InputValidation.existence_name_validator(command)
        self._from_currency = Currency[command]
        if self._from_currency is not Currency.ARS:
            self._to_currency = Currency.ARS

    def _to_currency_input(self) -> None:
        self._console.print(CURRENCY_NAMES)
        self._console.print("Destination currency", style="bold green")
        command = input("TO: ").upper()
        InputValidation.existence_name_validator(command)
        self._to_currency = Currency[command]

    def _amount_input(self) -> None:
        self._console.print(
            "Introduce the amount in "
            f"{self._from_currency.name.upper()} "
            f"to be converted to {self._to_currency.name.upper()}",
            style="bold green",
        )
        command = input("AMOUNT: ")
        self._amount = float(command)

    def wrap(self) -> ConversionParams:
        while self._amount == 0 or not self._from_currency or not self._to_currency:
            try:
                if not self._from_currency:
                    self._from_currency_input()
                if not self._to_currency:
                    self._to_currency_input()
                if self._amount == 0:
                    self._amount_input()
            except ValueError:
                self._console.print("Invalid value, please try again", style="bold red")
                continue
            return ConversionParams(
                exchange=self._exchange_data,
                console=self._console,
                amount=self._amount,
                from_currency=self._from_currency.value,
                to_currency=self._to_currency.value,
            )
