from pathlib import Path

import pytest

from strategy import ConsoleStrategy, FileStrategy, UpperFileStrategy


def test_console_strategy_prints_message(capsys: pytest.CaptureFixture[str]) -> None:
    ConsoleStrategy().write("2026-01-02 03:04:05 [INFO] hello")

    assert capsys.readouterr().out == "2026-01-02 03:04:05 [INFO] hello\n"


def test_file_strategy_writes_message_and_creates_directories(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "nested" / "app.log"

    FileStrategy(log_file).write("2026-01-02 03:04:05 [WARN] careful")

    assert log_file.read_text(encoding="utf-8") == "2026-01-02 03:04:05 [WARN] careful\n"


def test_file_strategy_appends_messages(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    strategy = FileStrategy(log_file)

    strategy.write("first")
    strategy.write("second")

    assert log_file.read_text(encoding="utf-8") == "first\nsecond\n"


def test_upper_file_strategy_uppercases_message(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"

    UpperFileStrategy(log_file).write("2026-01-02 03:04:05 [ERROR] Something happened")

    assert log_file.read_text(encoding="utf-8") == (
        "2026-01-02 03:04:05 [ERROR] SOMETHING HAPPENED\n"
    )
