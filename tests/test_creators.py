from pathlib import Path

import pytest

from abstract import AbstractLoggerFactory
from factory import (
    ConsoleLoggerFactoryCreator,
    FileLoggerFactoryCreator,
    UpperFileLoggerCreator,
)
from strategy import ConsoleStrategy, FileStrategy, UpperFileStrategy


def test_console_creator_creates_console_strategy() -> None:
    strategy = ConsoleLoggerFactoryCreator().create_strategy()

    assert isinstance(strategy, ConsoleStrategy)


def test_file_creator_creates_file_strategy() -> None:
    strategy = FileLoggerFactoryCreator("app.log").create_strategy()

    assert isinstance(strategy, FileStrategy)


def test_upper_file_creator_creates_upper_file_strategy() -> None:
    strategy = UpperFileLoggerCreator("app.log").create_strategy()

    assert isinstance(strategy, UpperFileStrategy)


def test_file_creator_passes_log_file_to_strategy(tmp_path: Path) -> None:
    log_file = tmp_path / "nested" / "app.log"

    FileLoggerFactoryCreator(log_file).create_strategy().write("line")

    assert log_file.read_text(encoding="utf-8") == "line\n"


def test_abstract_factory_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        AbstractLoggerFactory()
