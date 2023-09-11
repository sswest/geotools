import csv

import pytest

from geodev.coord import (
    bd09_to_wgs84,
    wgs84_to_bd09,
    gcj02_to_wgs84,
    wgs84_to_gcj02,
    bd09_to_gcj02,
)


def mock_data(filepath):
    data = []
    with open(filepath, "r") as f:
        cf = csv.DictReader(f, fieldnames=["wgs84", "bd09", "gcj02"])
        for row in cf:
            row["wgs84"] = list(map(float, row["wgs84"].split(",")))
            row["bd09"] = list(map(float, row["bd09"].split(",")))
            row["gcj02"] = list(map(float, row["gcj02"].split(",")))
            data.append(row)
    return data


# Replace 'your_module' with the actual module where your coordinate conversion functions are defined
@pytest.fixture
def mock_wgs84():
    return mock_data("tests/mock_wgs84.csv")


@pytest.fixture
def mock_bd09():
    return mock_data("tests/mock_bd09.csv")


@pytest.fixture
def mock_gcj02():
    return mock_data("tests/mock_bd09.csv")


# Test cases for bd09_to_wgs84
def test_bd09_to_wgs84(mock_bd09):
    for case in mock_bd09:
        result = bd09_to_wgs84(*case["bd09"])
        assert pytest.approx(result[0], 0.00001) == case["wgs84"][0]
        assert pytest.approx(result[1], 0.00001) == case["wgs84"][1]


# Test cases for wgs84_to_bd09
def test_wgs84_to_bd09(mock_wgs84):
    for case in mock_wgs84:
        result = wgs84_to_bd09(*case["wgs84"])
        assert pytest.approx(result[0], 0.00001) == case["bd09"][0]
        assert pytest.approx(result[1], 0.00001) == case["bd09"][1]


# Test cases for gcj02_to_wgs84
def test_gcj02_to_wgs84(mock_gcj02):
    for case in mock_gcj02:
        result = gcj02_to_wgs84(*case["gcj02"])
        assert pytest.approx(result[0], 0.00001) == case["wgs84"][0]
        assert pytest.approx(result[1], 0.00001) == case["wgs84"][1]


# Test cases for wgs84_to_gcj02
def test_wgs84_to_gcj02(mock_wgs84):
    for case in mock_wgs84:
        result = wgs84_to_gcj02(*case["wgs84"])
        assert pytest.approx(result[0], 0.00001) == case["gcj02"][0]
        assert pytest.approx(result[1], 0.00001) == case["gcj02"][1]


# Test cases for bd09_to_gcj02
def test_bd09_to_gcj02(mock_bd09):
    for case in mock_bd09:
        result = bd09_to_gcj02(*case["bd09"])
        assert pytest.approx(result[0], 0.00001) == case["gcj02"][0]
        assert pytest.approx(result[1], 0.00001) == case["gcj02"][1]
