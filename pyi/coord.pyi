from __future__ import annotations

def out_of_china(lon: float, lat: float) -> bool:
    """判断经纬度是否在中国境外
    :param lon: 经度
    :param lat: 纬度
    :return: 在中国境外返回True, 否则返回False
    """
    pass

def bd09_to_wgs84(lon: float, lat: float) -> tuple[float, float]:
    """百度坐标系(BD-09)转WGS坐标
    :param lon: 百度坐标经度
    :param lat: 百度坐标纬度
    :return: WGS84坐标经纬度
    """
    pass

def wgs84_to_bd09(lon: float, lat: float) -> tuple[float, float]:
    """WGS坐标转百度坐标系(BD-09)
    :param lon: WGS84坐标系的经度
    :param lat: WGS84坐标系的纬度
    :return: 百度坐标经纬度
    """
    pass

def gcj02_to_wgs84(lon: float, lat: float) -> tuple[float, float]:
    """火星坐标系(GCJ-02)转WGS84坐标
    :param lon: 火星坐标经度
    :param lat: 火星坐标纬度
    :return: WGS84坐标经纬度
    """
    pass

def bd09_to_gcj02(lon: float, lat: float) -> tuple[float, float]:
    """百度坐标系(BD-09)转火星坐标系(GCJ-02)
    :param lon: 百度坐标经度
    :param lat: 百度坐标纬度
    :return: 火星坐标经纬度
    """
    pass

def gcj02_to_bd09(lon: float, lat: float) -> tuple[float, float]:
    """火星坐标系(GCJ-02)转百度坐标系(BD-09)
    :param lon: 火星坐标经度
    :param lat: 火星坐标纬度
    :return: 百度坐标经纬度
    """
    pass

def wgs84_to_gcj02(lon: float, lat: float) -> tuple[float, float]:
    """WGS84坐标转火星坐标系(GCJ-02)
    :param lon: WGS84坐标系的经度
    :param lat: WGS84坐标系的纬度
    :return: 火星坐标经纬度
    """
    pass
