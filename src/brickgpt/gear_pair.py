"""Ideal, unshifted external spur gears on fixed, parallel Z axes (millimetres).

This checks assembly parameters, not tooth meshes or surrounding solids.
Initial tooth phase is assumed to be aligned by the assembler.
"""

import argparse
import json
import math
from pathlib import Path


def validate_pair(assembly: dict) -> dict:
    """Validate external JSON input and report ideal kinematic compatibility."""
    gears = assembly['gears']
    if len(gears) != 2:
        raise ValueError('Exactly two gears are required')
    for gear in gears:
        if type(gear['teeth']) is not int or gear['teeth'] < 3:
            raise ValueError('teeth must be an integer >= 3')
        for key in ('module_mm', 'width_mm', 'pressure_angle_deg'):
            value = gear[key]
            if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                raise ValueError(f'{key} must be a finite positive number')
        if gear['pressure_angle_deg'] >= 90:
            raise ValueError('pressure_angle_deg must be < 90')
        if len(gear['center_mm']) != 3 or any(
            type(v) not in (int, float) or not math.isfinite(v) for v in gear['center_mm']
        ):
            raise ValueError('center_mm must contain three finite numbers')
        if gear['joint'] not in ('revolute_z', 'fixed'):
            raise ValueError('joint must be revolute_z or fixed')

    a, b = gears
    errors = []
    if not math.isclose(a['module_mm'], b['module_mm'], rel_tol=0, abs_tol=1e-9):
        errors.append('module_mismatch')
    if not math.isclose(a['pressure_angle_deg'], b['pressure_angle_deg'], rel_tol=0, abs_tol=1e-9):
        errors.append('pressure_angle_mismatch')
    distance = math.hypot(a['center_mm'][0] - b['center_mm'][0],
                          a['center_mm'][1] - b['center_mm'][1])
    expected = (a['module_mm'] * a['teeth'] + b['module_mm'] * b['teeth']) / 2
    # Numerical tolerance only; manufacturing clearance is outside this model.
    if not math.isclose(distance, expected, rel_tol=0, abs_tol=1e-6):
        errors.append('center_distance_mismatch')
    overlap = min(a['center_mm'][2] + a['width_mm'] / 2,
                  b['center_mm'][2] + b['width_mm'] / 2) - max(
                      a['center_mm'][2] - a['width_mm'] / 2,
                      b['center_mm'][2] - b['width_mm'] / 2)
    if overlap <= 0:
        errors.append('no_axial_overlap')
    if any(g['joint'] != 'revolute_z' for g in gears):
        errors.append('rotation_blocked')
    return {
        'ideal_pair_compatible': not errors,
        'errors': errors,
        'center_distance_mm': distance,
        'required_center_distance_mm': expected,
        'axial_overlap_mm': max(0, overlap),
        'output_per_input_rotation': -a['teeth'] / b['teeth'] if not errors else None,
        'scope': 'ideal_external_spur_pair; aligned_phase; no_mesh_or_obstacle_check',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('assembly', type=Path, help='JSON assembly file')
    parser.add_argument('--input-deg', type=float, default=360, help='Input rotation increment')
    args = parser.parse_args()
    if not math.isfinite(args.input_deg):
        parser.error('--input-deg must be finite')
    result = validate_pair(json.loads(args.assembly.read_text(encoding='utf-8')))
    if result['ideal_pair_compatible']:
        result['input_delta_deg'] = args.input_deg
        result['output_delta_deg'] = args.input_deg * result['output_per_input_rotation']
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['ideal_pair_compatible'] else 1)


if __name__ == '__main__':
    main()
