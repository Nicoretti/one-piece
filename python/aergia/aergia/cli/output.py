from aergia._logging import logger
from rich.console import Console


class StatusOutput:

    def __init__(self, stderr, logger):
        self._stderr = stderr
        self._logger = logger

    @property
    def stderr(self):
        return self._stderr

    @property
    def logger(self):
        return self._logger

    def print(self, message, *args, **kwargs):
        self._logger.info(message, *args, **kwargs)
        self._stderr.print(message, *args, **kwargs)


stdout = Console()
stderr = StatusOutput(
    stderr=Console(stderr=True),
    logger=logger
)
