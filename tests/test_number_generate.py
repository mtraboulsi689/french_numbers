import runpy
from pathlib import Path

import pytest


MODULE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'number_generate.py'))
written_form = MODULE['written_form']
find_base_number = MODULE['find_base_number']


@pytest.mark.parametrize('number, expected', [
    (0, 'zero'),
    (1, 'un'),
    (10, 'dix'),
    (11, 'onze'),
    (17, 'dix-sept'),
    (20, 'vingt'),
    (21, 'vingt et un'),
    (70, 'soixante-dix'),
    (71, 'soixante-et-onze'),
    (80, 'quatre-vingts'),
    (81, 'quatre-vingt-un'),
    (90, 'quatre-vingt-dix'),
    (99, 'quatre-vingt-dix-neuf'),
    (100, 'cent'),
    (101, 'cent un'),
    (200, 'deux cents'),
    (201, 'deux cent un'),
    (999, 'neuf cent quatre-vingt-dix-neuf'),
    (1000, 'un mille'),
    (1001, 'un mille un'),
    (2000, 'deux mille'),
])
def test_written_form(number, expected):
    assert written_form(number) == expected


@pytest.mark.parametrize('number, expected', [
    ('000', ''),
    ('007', 'sept'),
    ('021', 'vingt et un'),
    ('100', 'cent '),
    ('200', 'deux cents '),
    ('201', 'deux cent un'),
])
def test_find_base_number(number, expected):
    assert find_base_number(number) == expected


@pytest.mark.parametrize('number, expected', [
    (1000000, 'un million  mille'),
    (2000000, 'deux millions  mille'),
    (1000000000, 'un milliard  millions  mille'),
    (1000000000000, 'un billion  milliards  millions  mille'),
    (1000000000000000, ''),
])
def test_written_form_large_numbers_current_behavior(number, expected):
    # Preserve existing zero-group labels and spacing until a separate bug fix.
    assert written_form(number) == expected
