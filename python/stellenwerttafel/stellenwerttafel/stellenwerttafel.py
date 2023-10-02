import textual
import logging
from textual import containers
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static, Digits, Rule
from textual.logging import TextualHandler

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)


class Position(Static):

    def __init__(self, name: str, init_value: int = 0, classes: str = ''):
        super().__init__(classes=classes)
        self._name = name
        self._value = init_value

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield containers.Vertical(
            Static(self._name),
            Button("+", id="increment", classes=" ".join(self.classes)),
            Digits(f"{self._value}", id=f"{self._name.lower()}", classes=" ".join(self.classes)),
            Button("-", id="decrement", classes=" ".join(self.classes)),
            classes=' '.join(self.classes)
        )


class StellenWertTafel(Static):
    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield containers.Horizontal(
            Position("Tausender", 0, classes='t'),
            Position("Hunderter", 100, 'h'),
            Position("Zehner", 0, classes='z'),
            Position("Einer", 0, classes='e'),
        )


class Status(Static):

    def compose(self) -> ComposeResult:
        yield Static("Mode: <Einer>")
        yield containers.Horizontal(
            Static("Aktuelle Zahl:"),
            containers.Horizontal(

                Digits("0"),
                Digits("0"),
                Digits("0"),
                Digits("0"),
            )
        )


class Mode(Static):
    def compose(self) -> ComposeResult:
        yield Button(label="Mode: <unknown>", id='mode')


class Stellenwerte(App):
    """A Textual app to learn about positional value systems."""

    CSS_PATH = 'stellenwerttafel.css'
    SUB_TITLE = 'Dezimalsystem'

    BINDINGS = [
        ("+", "inc", "Increment"),
        ("-", "dec", "Decrement"),
        ("m", "Mode", "Toggle current mode"),
        ("e", "einer", "Einer Mode"),
        ("z", "zehner", "Zehner Mode"),
        ("h", "hunderter", "Hundeter Mode"),
        ("t", "tausender", "Tausender Mode"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    MODES = ['Tausender', "Hunderter", "Zehner", "Einer"]
    _mode: str

    def __init__(self):
        super().__init__()
        self._mode = self.MODES[-1]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Rule()
        yield Status()
        yield Rule()
        yield StellenWertTafel()
        yield Rule()
        yield Footer()

    def action_inc(self) -> None:
        position = self.query_one(self._mode.lower())
        position._value = f"{int(position._value) + 1}"

    def action_dec(self) -> None:
        position = self.query_one(self._mode.lower())
        position._value = f"{int(position._value) - 1}"

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_log(self) -> None:
        logging.debug("Logging right now")
        logging.info("Logging right now")

    def action_help(self) -> None:
        self.mount(textual.widgets.Welcome())


if __name__ == "__main__":
    app = Stellenwerte()
    app.run()
