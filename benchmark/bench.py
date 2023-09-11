import time
import random
import timeit

import numpy as np
from geodev import vec, coord

from coordinate import Coordinate

locs = [(random.randrange(72, 137), random.randrange(0, 56)) for _ in range(10000)]
locs_ = np.array(locs)
co = Coordinate()


def out_of_china(longitude, latitude):
    """

    :param longitude:
    :param latitude:
    :return:
    """
    if longitude < 72.004 or longitude > 137.8347:
        return True
    if latitude < 0.8293 or latitude > 55.8271:
        return True
    return False


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} cost {time.time() - start} seconds")
        return res

    return wrapper


def test_vec():
    vec.out_of_china(locs_)


def test_coord():
    for loc in locs:
        coord.out_of_china(*loc)


def test_py():
    for loc in locs:
        out_of_china(*loc)


def test_bd09_to_wgs84():
    for loc in locs:
        x, y = coord.bd09_to_wgs84(*loc)


def test_bd09_to_wgs84_numpy():
    vec.bd09_to_wgs84(locs_)


def test_bd09_to_wgs84_py():
    for loc in locs:
        x, y = co.bd09_to_wgs84(*loc)


def test_bd09_to_gcj02():
    for loc in locs:
        x, y = coord.bd09_to_gcj02(*loc)


def test_bd09_to_gcj02_numpy():
    vec.bd09_to_gcj02(locs_)


def test_bd09_to_gcj02_py():
    for loc in locs:
        x, y = co.bd09_to_gcj02(*loc)


def test_gcj02_to_bd09():
    for loc in locs:
        x, y = coord.gcj02_to_bd09(*loc)


def test_gcj02_to_bd09_numpy():
    vec.gcj02_to_bd09(locs_)


def test_gcj02_to_bd09_py():
    for loc in locs:
        x, y = co.gcj02_to_bd09(*loc)


def test_gcj02_to_wgs84():
    for loc in locs:
        x, y = coord.gcj02_to_wgs84(*loc)


def test_gcj02_to_wgs84_numpy():
    vec.gcj02_to_wgs84(locs_)


def test_gcj02_to_wgs84_py():
    for loc in locs:
        x, y = co.gcj02_to_wgs84(*loc)


def test_wgs84_to_bd09():
    for loc in locs:
        x, y = coord.wgs84_to_bd09(*loc)


def test_wgs84_to_bd09_numpy():
    vec.wgs84_to_bd09(locs_)


def test_wgs84_to_bd09_py():
    for loc in locs:
        x, y = co.wgs84_to_bd09(*loc)


def test_wgs84_to_gcj02():
    for loc in locs:
        x, y = coord.wgs84_to_gcj02(*loc)


def test_wgs84_to_gcj02_numpy():
    vec.wgs84_to_gcj02(locs_)


def test_wgs84_to_gcj02_py():
    for loc in locs:
        x, y = co.wgs84_to_gcj02(*loc)


def run_tests():
    test_functions = [
        [
            test_bd09_to_wgs84_py,
            test_bd09_to_wgs84,
            test_bd09_to_wgs84_numpy,
        ],
        [
            test_bd09_to_gcj02_py,
            test_bd09_to_gcj02,
            test_bd09_to_gcj02_numpy,
        ],
        [
            test_gcj02_to_wgs84_py,
            test_gcj02_to_wgs84,
            test_gcj02_to_wgs84_numpy,
        ],
        [
            test_gcj02_to_bd09_py,
            test_gcj02_to_bd09,
            test_gcj02_to_bd09_numpy,
        ],
        [
            test_wgs84_to_bd09_py,
            test_wgs84_to_bd09,
            test_wgs84_to_bd09_numpy,
        ],
        [
            test_wgs84_to_gcj02_py,
            test_wgs84_to_gcj02,
            test_wgs84_to_gcj02_numpy,
        ],
    ]

    for (py_func, c_ext, vec_func) in test_functions:
        py_elapsed = timeit.timeit(py_func, number=10)
        c_elapsed = timeit.timeit(c_ext, number=10)
        vec_elapsed = timeit.timeit(vec_func, number=10)
        print(f"{py_func.__name__} took {py_elapsed:.6f} seconds")
        print(f"{c_ext.__name__} took {c_elapsed:.6f} seconds")
        print(f"{vec_func.__name__} took {vec_elapsed:.6f} seconds")
        print(f"{c_ext.__name__} compare {py_func.__name__} improve {((py_elapsed-c_elapsed)/c_elapsed):.0%}")
        print(f"{vec_func.__name__} compare {py_func.__name__} improve {((py_elapsed-vec_elapsed)/vec_elapsed):.0%}")


if __name__ == "__main__":
    run_tests()
