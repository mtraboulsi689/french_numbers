import runpy
from pathlib import Path

import pytest


@pytest.fixture
def game(monkeypatch, capsys):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root))
    monkeypatch.setattr('os.system', lambda command: 0)
    monkeypatch.setattr('builtins.input', lambda *args: '0')
    namespace = runpy.run_path(str(root / 'numbers.py'))
    capsys.readouterr()
    return namespace


@pytest.mark.parametrize('answer, candidates, expected', [
    ('VINGT ET UN', ['vingt et un'], True),
    ('answer: vingt et un', ['vingt et un'], True),
    ('vingt', ['vingt et un'], False),
    ('quit', ['quit', 'exit'], True),
    ('exit', ['quit', 'exit'], False),
    ('anything', [], None),
])
def test_validate_current_behavior(game, answer, candidates, expected):
    assert game['validate'](answer, candidates) is expected


@pytest.mark.parametrize('points, level, expected_points, expected_level', [
    (3, 1, 3, 1),
    (-2, 1, 0, 1),
    (10, 1, 0, 2),
])
def test_base_game_scoring(game, monkeypatch, points, level,
                           expected_points, expected_level):
    monkeypatch.setattr('random.randint', lambda low, high: high)
    number, score, current_level, levels = game['base_game'](points, level)
    assert levels == [100, 1000, 10000, 100000, 1000000]
    assert number == levels[level - 1]
    assert (score, current_level) == (expected_points, expected_level)


def test_base_game_win(game, capsys):
    assert game['base_game'](points=10, level=5) == (-1, -1, -1, [])
    assert 'Congratulations! You won the game!' in capsys.readouterr().out
