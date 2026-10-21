import copy
import json
from pathlib import Path

import pytest

from brickgpt.gear_pair import validate_pair


@pytest.fixture
def assembly():
    return json.loads((Path(__file__).parents[1] / 'examples/gears/valid.json').read_text())


def test_valid_transmission(assembly):
    result = validate_pair(assembly)
    assert result['ideal_pair_compatible']
    assert result['errors'] == []
    assert result['output_per_input_rotation'] * 360 == -180


@pytest.mark.parametrize(('field', 'value', 'error'), [
    ('center_mm', [35, 0, 0], 'center_distance_mismatch'),
    ('center_mm', [30, 0, 5], 'no_axial_overlap'),
    ('module_mm', 2, 'module_mismatch'),
    ('pressure_angle_deg', 25, 'pressure_angle_mismatch'),
    ('joint', 'fixed', 'rotation_blocked'),
])
def test_invalid_assembly(assembly, field, value, error):
    assembly['gears'][1][field] = value
    result = validate_pair(assembly)
    assert not result['ideal_pair_compatible']
    assert error in result['errors']
    assert result['output_per_input_rotation'] is None


def test_rotated_layout_and_partial_overlap(assembly):
    assembly['gears'][1]['center_mm'] = [18, 24, 4]
    assert validate_pair(assembly)['ideal_pair_compatible']


@pytest.mark.parametrize(('field', 'value'), [
    ('teeth', 20.5), ('teeth', True), ('module_mm', 0),
    ('width_mm', -1), ('pressure_angle_deg', 90),
    ('center_mm', [0, 0, float('nan')]), ('joint', 'unknown'),
])
def test_malformed_input(assembly, field, value):
    assembly['gears'][0][field] = value
    with pytest.raises(ValueError):
        validate_pair(assembly)


def test_requires_two_gears(assembly):
    assembly['gears'].append(copy.deepcopy(assembly['gears'][0]))
    with pytest.raises(ValueError):
        validate_pair(assembly)
