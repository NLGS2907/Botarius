"""
Events Register.
"""

from logging import INFO, FileHandler, Formatter, StreamHandler, getLogger
from typing import TYPE_CHECKING

from ..auxiliar import Singleton
from ..db.shortcuts import get_log_path

if TYPE_CHECKING:

    from logging import Logger


class BotLogger(metaclass=Singleton):
    """
    Class for registering bot events.
    Made with singleton pattern.
    """

    def __new__(cls) -> "BotLogger":
        """
        Returns the class instance,
        which is unique.
        """

        if not hasattr(cls, "_instance"):
            cls._instancia = super(BotLogger, cls).__new__(cls)

        return cls._instancia


    def __init__(self,
                 *,
                 log_name: str="botarius",
                 log_level: int=INFO,
                 fmt: str="[ %(asctime)s ] [ %(levelname)s ] %(message)s",
                 fmt_date: str="%d-%m-%Y %I:%M:%S %p") -> None:
        """
        Initializes an instace of 'BotLogger'.
        """

        super().__init__()

        self._format: str = fmt
        self._fmt_date: str = fmt_date

        self._formatter = Formatter(fmt=self.format, datefmt=self.fmt_date)

        self.file_handler = FileHandler(filename=get_log_path(), encoding="utf-8")
        self.stream_handler = StreamHandler()
        self.update_formatter()

        self.logger: "Logger" = getLogger(log_name)
        self.logger.setLevel(log_level)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)


    def update_formatter(self) -> None:
        """
        Updates the formatter for each handler the logger has.
        """

        self.file_handler.setFormatter(self.formatter)
        self.stream_handler.setFormatter(self.formatter)


    @property
    def formatter(self) -> Formatter:
        """
        Returns the formatter in use.
        """

        return self._formatter

    @formatter.setter
    def formatter(self, new_formatter: Formatter) -> None:

        self._formatter = new_formatter
        self.update_formatter()


    @property
    def format(self) -> str:
        """
        Returns the format of the log messages.
        """

        return self._format


    @format.setter
    def format(self, new_format) -> None:

        self._format = new_format
        self.formatter = Formatter(fmt=self.format, datefmt=self.fmt_date)


    @property
    def fmt_date(self) -> str:
        """
        Returns the date format of the log messages.
        """

        return self._fmt_date


    @fmt_date.setter
    def fmt_date(self, new_fmt_date: str) -> None:

        self._fmt_date = new_fmt_date
        self.formatter = Formatter(fmt=self.format, datefmt=self.fmt_date)


    def debug(self, message: str, *args, **kwargs) -> None:
        """
        Registers an event of DEBUG level.
        """

        self.logger.debug(message, *args, **kwargs)


    def info(self, message: str, *args, **kwargs) -> None:
        """
        Registers an event of INFO level.
        """

        self.logger.info(message, *args, **kwargs)


    def warning(self, message: str, *args, **kwargs) -> None:
        """
        Registers an event of WARNING level.
        """

        self.logger.warning(message, *args, **kwargs)


    def error(self, message: str, *args, **kwargs) -> None:
        """
        Registers an event of ERROR level.
        """

        self.logger.error(message, *args, **kwargs)


    def critical(self, message: str, *args, **kwargs) -> None:
        """
        Registers an event of CRITICAL level.
        """

        self.logger.critical(message, *args, **kwargs)


    def exception(self, message, *args, exc_info=True, **kwargs) -> None:
        """
        Registers an exception.
        """

        self.logger.exception(message, *args, exc_info, **kwargs)
