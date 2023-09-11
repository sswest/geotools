from __future__ import annotations

from typing import TypeAlias

from numpy import ndarray

Sequence: TypeAlias = list | tuple | ndarray


def out_of_china(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组经纬度是否在中国境外
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: bool数组
    """
    pass


def bd09_to_wgs84(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组bd09经纬度转换为wgs84
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: 新的经纬度数组 [经度, 纬度]
    """
    pass


def bd09_to_gcj02(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组bd09经纬度转换为gcj02
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: 新的经纬度数组 [经度, 纬度]
    """
    pass


def gcj02_to_bd09(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组gcj02经纬度转换为bd09
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: 新的经纬度数组 [经度, 纬度]
    """
    pass


def gcj02_to_wgs84(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组gcj02经纬度转换为wgs84
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: 新的经纬度数组 [经度, 纬度]
    """
    pass


def wgs84_to_gcj02(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组wgs84经纬度转换为gcj02
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: 新的经纬度数组 [经度, 纬度]
    """
    pass


def wgs84_to_bd09(loc_array: list[float] | tuple[float, float] | ndarray) -> ndarray:
    """判断一组wgs84经纬度转换为bd09
    :param loc_array: 经纬度数组 [经度, 纬度]
    :return: 新的经纬度数组 [经度, 纬度]
    """
    pass
