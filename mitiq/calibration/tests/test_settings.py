# Copyright (C) 2021 Unitary Fund
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import pytest

from mitiq.calibration import ZNESettings, Settings
from mitiq.zne.scaling import fold_global, fold_gates_at_random
from mitiq.zne.inference import RichardsonFactory, ExpFactory, LinearFactory


def test_basic_settings():
    settings = Settings(
        ["zne"],
        circuit_types=["ghz"],
        num_qubits=2,
        circuit_depth=999,
        technique_params={
            "scale_factors": [[1, 3, 4]],
            "scale_methods": [fold_global, fold_gates_at_random],
            "factories": [RichardsonFactory, ExpFactory, LinearFactory],
        },
    )
    circuits = settings.make_circuits()
    assert len(circuits) == 1
    ghz_problem = circuits[0]
    assert len(ghz_problem.circuit) == 2
    assert ghz_problem.two_qubit_gate_count == 1
    assert ghz_problem.ideal_distribution == {"00": 0.5, "11": 0.5}

    strategies = settings.make_strategies()
    num_strategies = 1 * 2 * 3
    assert len(strategies) == num_strategies


def test_make_circuits_qv_circuits():
    settings = Settings(
        ["zne"],
        circuit_types=["qv"],
        num_qubits=2,
        circuit_depth=999,
        technique_params={
            "scale_factors": [[1, 3, 4]],
            "scale_methods": [fold_global, fold_gates_at_random],
            "factories": [RichardsonFactory, ExpFactory, LinearFactory],
        },
    )
    with pytest.raises(NotImplementedError, match="quantum volume circuits"):
        settings.make_circuits()


def test_make_circuits_invalid_circuit_type():
    settings = Settings(
        ["zne"],
        circuit_types=["foobar"],
        num_qubits=2,
        circuit_depth=999,
        technique_params={
            "scale_factors": [[1, 3, 4]],
            "scale_methods": [fold_global, fold_gates_at_random],
            "factories": [RichardsonFactory, ExpFactory, LinearFactory],
        },
    )
    with pytest.raises(
        ValueError, match="invalid value passed for `circuit_types`"
    ):
        settings.make_circuits()


def test_make_strategies_invalid_method():
    settings = Settings(
        ["destroy_my_errors"],
        circuit_types=["shor"],
        num_qubits=2,
        circuit_depth=999,
        technique_params={
            "scale_factors": [[1, 3, 4]],
            "scale_methods": [fold_global, fold_gates_at_random],
            "factories": [RichardsonFactory, ExpFactory, LinearFactory],
        },
    )
    with pytest.raises(ValueError, match="Invalid value passed"):
        settings.make_strategies()


def test_ZNESettings():
    circuits = ZNESettings.make_circuits()
    strategies = ZNESettings.make_strategies()

    assert len(circuits) == 3
    assert len(strategies) == 2 * 2 * 2
