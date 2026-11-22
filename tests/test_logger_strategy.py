import re
from pathlib import Path

import pytest

from creators import (
    ConsoleStrategyCreator,
    FileStrategyCreator,
    UpperFileStrategyCreator,
)
from logger import ConsoleOutputStrategy, Logger, LogLevel


# Тест проверяет вывод отформатированного сообщения в консоль.
def test_console_strategy_prints_formatted_message(capsys: pytest.CaptureFixture[str]) -> None:
    logger = Logger(ConsoleStrategyCreator())

    result = logger.log(LogLevel.INFO, "Application started")

    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \[INFO\] Application started", result)
    assert result in capsys.readouterr().out


# Тест проверяет создание каталога и запись сообщения в файл.
def test_file_strategy_appends_message(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "app.log"
    logger = Logger(FileStrategyCreator(), path)

    result = logger.log(LogLevel.WARN, "Low disk space")

    text = path.read_text(encoding="utf-8")
    assert "[WARN] Low disk space" in text
    assert text.endswith("\n")
    assert result in text


# Тест проверяет запись всей отформатированной строки в верхнем регистре.
def test_upper_file_strategy_writes_uppercase(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    logger = Logger(UpperFileStrategyCreator(), path)

    logger.log(LogLevel.ERROR, "Something happened")

    text = path.read_text(encoding="utf-8")
    assert "[ERROR] SOMETHING HAPPENED" in text


# Тест проверяет допустимое преобразование строкового уровня в LogLevel.
def test_string_log_level_is_accepted() -> None:
    logger = Logger(ConsoleStrategyCreator())

    result = logger.log("TRACE", "Trace message")

    assert "[TRACE] Trace message" in result


# Негативный тест проверяет отклонение неизвестного строкового уровня.
def test_unknown_string_log_level_is_rejected() -> None:
    logger = Logger(ConsoleStrategyCreator())

    try:
        logger.log("DEBUG", "Debug message")
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалось исключение ValueError")


# Негативный тест проверяет отклонение сообщения неверного типа.
def test_non_string_message_is_rejected() -> None:
    logger = Logger(ConsoleStrategyCreator())

    try:
        logger.log(LogLevel.INFO, 123)
    except TypeError:
        pass
    else:
        raise AssertionError("Ожидалось исключение TypeError")


# Тест проверяет возможность явной замены текущей Strategy.
def test_strategy_can_be_changed() -> None:
    logger = Logger(ConsoleStrategyCreator())

    logger.set_strategy(ConsoleOutputStrategy())

    result = logger.log(LogLevel.FATAL, "Fatal message")
    assert "[FATAL] Fatal message" in result


# Негативный тест проверяет отклонение объекта, не реализующего интерфейс Creator или Strategy.
def test_non_creator_object_is_rejected() -> None:
    try:
        Logger(object())
    except TypeError:
        pass
    else:
        raise AssertionError("Ожидалось исключение TypeError")


# Тест проверяет форматирование всех допустимых уровней журнала.
def test_all_log_levels_are_accepted() -> None:
    logger = Logger(ConsoleStrategyCreator())

    levels = ["TRACE", "INFO", "WARN", "ERROR", "FATAL"]

    for level in levels:
        result = logger.log(level, "Проверка")
        assert f"[{level}] Проверка" in result


# Негативный тест проверяет отклонение уровня со значением None.
def test_none_log_level_is_rejected() -> None:
    logger = Logger(ConsoleStrategyCreator())

    try:
        logger.log(None, "Сообщение")
    except TypeError:
        pass
    else:
        raise AssertionError("Ожидалось исключение TypeError")


# Негативный тест проверяет отклонение объекта, не реализующего интерфейс Strategy.
def test_non_strategy_object_is_rejected() -> None:
    try:
        logger = Logger(ConsoleStrategyCreator())
        logger.set_strategy(object())
    except TypeError:
        pass
    else:
        raise AssertionError("Ожидалось исключение TypeError")
