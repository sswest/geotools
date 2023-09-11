"""坐标系转换"""
import math


class Coordinate:
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    pi = 3.1415926535897932384626
    a = 6378245.0
    ee = 0.00669342162296594323

    @classmethod
    def bd09_to_wgs84(cls, lng, lat):
        gcj_location = cls.bd09_to_gcj02(lng, lat)
        return cls.gcj02_to_wgs84(gcj_location[0], gcj_location[1])

    @classmethod
    def bd09_to_gcj02(cls, lng, lat):
        x = lng - 0.0065
        y = lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * cls.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * cls.x_pi)

        return [z * math.cos(theta), z * math.sin(theta)]

    @classmethod
    def gcj02_to_wgs84(cls, lng, lat):
        if cls.out_of_china(lng, lat):
            return lng, lat

        dlat = cls.transform_latitude(lng - 105, lat - 35)
        dlng = cls.transform_longitude(lng - 105, lat - 35)
        rad_lat = lat / 180 * cls.pi
        magic = math.sin(rad_lat)
        magic = 1 - cls.ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        dlat = (dlat * 180) / ((cls.a * (1 - cls.ee)) / (magic * sqrt_magic) * cls.pi)
        dlng = (dlng * 180) / (cls.a / sqrt_magic * math.cos(rad_lat) * cls.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    @classmethod
    def gcj02_to_bd09(cls, lng, lat):
        """
        :param lng:
        :param lat:
        :return:
        """

        if lng == 0 and lat == 0:
            return [0, 0]

        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * cls.x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * cls.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lng, bd_lat]

    @classmethod
    def wgs84_to_bd09(cls, lng, lat):
        """
        :param lng:
        :param lat:
        :return:
        """
        if lng == 0 and lat == 0:
            return [0, 0]

        gcj02_data = cls.wgs84_to_gcj02(lng, lat)
        return cls.gcj02_to_bd09(gcj02_data[0], gcj02_data[1])

    @classmethod
    def wgs84_to_gcj02(cls, lng, lat):
        """
        :param lng:
        :param lat:
        :return:
        """
        if cls.out_of_china(lng, lat):  # 判断是否在国内
            return [lng, lat]

        dlat = cls.transform_latitude(lng - 105, lat - 35)
        dlng = cls.transform_longitude(lng - 105, lat - 35)
        radlat = lat / 180 * cls.pi
        magic = math.sin(radlat)
        magic = 1 - cls.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180) / ((cls.a * (1 - cls.ee)) / (magic * sqrtmagic) * cls.pi)
        dlng = (dlng * 180) / (cls.a / sqrtmagic * math.cos(radlat) * cls.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [mglng, mglat]

    @classmethod
    def transform_latitude(cls, lng, lat):
        """
        :param lng:
        :param lat:
        :return:
        """
        ret = -100
        ret += (
            2 * lng
            + 3 * lat
            + 0.2 * lat * lat
            + 0.1 * lng * lat
            + 0.2 * math.sqrt(abs(lng))
        )
        ret += (
            (20 * math.sin(6 * lng * cls.pi) + 20 * math.sin(2 * lng * cls.pi)) * 2 / 3
        )
        ret += (20 * math.sin(lat * cls.pi) + 40 * math.sin(lat / 3 * cls.pi)) * 2 / 3
        ret += (
            (160 * math.sin(lat / 12 * cls.pi) + 320 * math.sin(lat * cls.pi / 30.0))
            * 2
            / 3
        )
        return ret

    @classmethod
    def transform_longitude(cls, lng, lat):
        """
        :param lng:
        :param lat:
        :return:
        """
        ret = (
            300
            + lng
            + 2 * lat
            + 0.1 * lng * lng
            + 0.1 * lng * lat
            + 0.1 * math.sqrt(abs(lng))
        )
        ret += (
            (20 * math.sin(6 * lng * cls.pi) + 20 * math.sin(2 * lng * cls.pi)) * 2 / 3
        )
        ret += (
            (20 * math.sin(lng * cls.pi) + 40 * math.sin(lng / 3.0 * cls.pi))
            * 2.0
            / 3.0
        )
        ret += (
            (150 * math.sin(lng / 12 * cls.pi) + 300 * math.sin(lng / 30 * cls.pi))
            * 2
            / 3
        )
        return ret

    @staticmethod
    def out_of_china(lng, lat) -> bool:
        """
        :param lng:
        :param lat:
        :return:
        """
        if lng < 72.004 or lng > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False

    @classmethod
    def transfer(cls, source: str, target: str):
        name = f"{source}_to_{target}"
        return getattr(cls, name)
