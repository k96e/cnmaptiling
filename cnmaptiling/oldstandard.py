from .angle import Angle
from .scale import Scale
from math import floor

class OldStandard():
    """
    国家标准比例尺地形图旧图号
    """
    def __init__(self, scale: Scale):
        self.scale = scale
        
    def calc_1M(self, lon: Angle, lat: Angle) -> tuple[int, int]:
        """
        计算1:1M比例尺的图号
        """
        H = floor(lat/Scale.LEVEL_1M.lat_diff) + 1
        L = floor(lon/Scale.LEVEL_1M.lon_diff) + 31
        return H, L

    def calc_1M_reverse(self, H: int, L: int) -> tuple[Angle, Angle]:
        """
        计算1:1M比例尺的西南图廓点
        """
        lon = Scale.LEVEL_1M.lon_diff*(L-31)
        lat = Scale.LEVEL_1M.lat_diff*(H-1)
        return lon, lat

    def calc_step(self, lon: Angle, lat: Angle, scale: Scale, last_scale: Scale) -> int:
        """
        计算当前比例尺的序号
        """
        V = scale.nums*(scale.nums-1)+1
        v_lat = floor((lat%last_scale.lat_diff)/scale.lat_diff)
        v_lon = floor((lon%last_scale.lon_diff)/scale.lon_diff)
        return V - v_lat*scale.nums + v_lon

    def calc_reverse(self, last_lon: Angle, last_lat: Angle, scale: Scale, code: int) -> tuple[Angle, Angle]:
        """
        计算当前比例尺的西南图廓点
        """
        lon = last_lon + scale.lon_diff*((code-1)%scale.nums)
        lat = last_lat + scale.lat_diff*floor((scale.nums**2-code)/scale.nums)
        return lon, lat

    def latlon_to_oldstandard(self, lon: Angle, lat: Angle) -> str:
        """
        将经纬度转换为旧图号
        """
        H, L = self.calc_1M(lon, lat)
        H_code = chr(64 + H)
        if self.scale == Scale.LEVEL_1M:
            return f"{H_code}-{L}"
        elif self.scale == Scale.LEVEL_500K:
            a = self.calc_step(lon, lat, Scale.LEVEL_500K, Scale.LEVEL_1M)
            a_code = chr(64 + a)
            return f"{H_code}-{L}-{a_code}"
        elif self.scale == Scale.LEVEL_250K:
            a = self.calc_step(lon, lat, Scale.LEVEL_250K, Scale.LEVEL_1M)
            return f"{H_code}-{L}-[{a}]"
        elif self.scale == Scale.LEVEL_100K:
            a = self.calc_step(lon, lat, Scale.LEVEL_100K, Scale.LEVEL_1M)
            return f"{H_code}-{L}-{a}"
        elif self.scale == Scale.LEVEL_50K:
            a = self.calc_step(lon, lat, Scale.LEVEL_100K, Scale.LEVEL_1M)
            b = self.calc_step(lon, lat, Scale.LEVEL_50K, Scale.LEVEL_100K)
            b_code = chr(64 + b)
            return f"{H_code}-{L}-{a}-{b_code}"
        elif self.scale == Scale.LEVEL_25K:
            a = self.calc_step(lon, lat, Scale.LEVEL_100K, Scale.LEVEL_1M)
            b = self.calc_step(lon, lat, Scale.LEVEL_50K, Scale.LEVEL_100K)
            b_code = chr(64 + b)
            c = self.calc_step(lon, lat, Scale.LEVEL_25K, Scale.LEVEL_50K)
            return f"{H_code}-{L}-{a}-{b_code}-{c}"
        elif self.scale == Scale.LEVEL_10K:
            a = self.calc_step(lon, lat, Scale.LEVEL_100K, Scale.LEVEL_1M)
            b = self.calc_step(lon, lat, Scale.LEVEL_10K, Scale.LEVEL_100K)
            return f"{H_code}-{L}-{a}-({b})"
        elif self.scale == Scale.LEVEL_5K:
            a = self.calc_step(lon, lat, Scale.LEVEL_100K, Scale.LEVEL_1M)
            b = self.calc_step(lon, lat, Scale.LEVEL_10K, Scale.LEVEL_100K)
            c = self.calc_step(lon, lat, Scale.LEVEL_5K, Scale.LEVEL_10K)
            c_code = chr(96 + c)
            return f"{H_code}-{L}-{a}-({b})-{c_code}"
        raise ValueError(f"Invalid scale for old standard: {self.scale}")
    
    def oldstandard_to_latlon(self, code: str) -> tuple[tuple[Angle, Angle], tuple[Angle, Angle]]:
        """
        将旧图号转换为经纬度范围
        """
        if self.scale == Scale.LEVEL_1M:
            H, L = code.split("-")
            H = ord(H) - 64
            L = int(L)
            lon, lat = self.calc_1M_reverse(H, L)
            lon_ne = lon + Scale.LEVEL_1M.lon_diff
            lat_ne = lat + Scale.LEVEL_1M.lat_diff
            return (lon, lat), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_500K:
            H, L, a = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = ord(a) - 64
            lon, lat = self.calc_1M_reverse(H, L)
            lon_a, lat_a = self.calc_reverse(lon, lat, Scale.LEVEL_500K, a)
            lon_ne = lon_a + Scale.LEVEL_500K.lon_diff
            lat_ne = lat_a + Scale.LEVEL_500K.lat_diff
            return (lon_a, lat_a), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_250K:
            H, L, a = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = int(a[1:-1])
            lon, lat = self.calc_1M_reverse(H, L)
            lon_a, lat_a = self.calc_reverse(lon, lat, Scale.LEVEL_250K, a)
            lon_ne = lon_a + Scale.LEVEL_250K.lon_diff
            lat_ne = lat_a + Scale.LEVEL_250K.lat_diff
            return (lon_a, lat_a), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_100K:
            H, L, a = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = int(a)
            lon, lat = self.calc_1M_reverse(H, L)
            lon, lat = self.calc_reverse(lon, lat, Scale.LEVEL_100K, a)
            lon_ne = lon + Scale.LEVEL_100K.lon_diff
            lat_ne = lat + Scale.LEVEL_100K.lat_diff
            return (lon, lat), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_50K:
            H, L, a, b = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = int(a)
            b = ord(b) - 64
            lon, lat = self.calc_1M_reverse(H, L)
            lon_a, lat_a = self.calc_reverse(lon, lat, Scale.LEVEL_100K, a)
            lon_b, lat_b = self.calc_reverse(lon_a, lat_a, Scale.LEVEL_50K, b)
            lon_ne = lon_b + Scale.LEVEL_50K.lon_diff
            lat_ne = lat_b + Scale.LEVEL_50K.lat_diff
            return (lon_b, lat_b), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_25K:
            H, L, a, b, c = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = int(a)
            b = ord(b) - 64
            c = int(c)
            lon, lat = self.calc_1M_reverse(H, L)
            lon_a, lat_a = self.calc_reverse(lon, lat, Scale.LEVEL_100K, a)
            lon_b, lat_b = self.calc_reverse(lon_a, lat_a, Scale.LEVEL_50K, b)
            lon_c, lat_c = self.calc_reverse(lon_b, lat_b, Scale.LEVEL_25K, c)
            lon_ne = lon_c + Scale.LEVEL_25K.lon_diff
            lat_ne = lat_c + Scale.LEVEL_25K.lat_diff
            return (lon_c, lat_c), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_10K:
            H, L, a, b = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = int(a)
            b = int(b[1:-1])
            lon, lat = self.calc_1M_reverse(H, L)
            lon_a, lat_a = self.calc_reverse(lon, lat, Scale.LEVEL_100K, a)
            lon_b, lat_b = self.calc_reverse(lon_a, lat_a, Scale.LEVEL_10K, b)
            lon_ne = lon_b + Scale.LEVEL_10K.lon_diff
            lat_ne = lat_b + Scale.LEVEL_10K.lat_diff
            return (lon_b, lat_b), (lon_ne, lat_ne)
        elif self.scale == Scale.LEVEL_5K:
            H, L, a, b, c = code.split("-")
            H = ord(H) - 64
            L = int(L)
            a = int(a)
            b = int(b[1:-1])
            c = ord(c) - 96
            lon, lat = self.calc_1M_reverse(H, L)
            lon_a, lat_a = self.calc_reverse(lon, lat, Scale.LEVEL_100K, a)
            lon_b, lat_b = self.calc_reverse(lon_a, lat_a, Scale.LEVEL_10K, b)
            lon_c, lat_c = self.calc_reverse(lon_b, lat_b, Scale.LEVEL_5K, c)
            lon_ne = lon_c + Scale.LEVEL_5K.lon_diff
            lat_ne = lat_c + Scale.LEVEL_5K.lat_diff
            return (lon_c, lat_c), (lon_ne, lat_ne)
        raise ValueError(f"Invalid scale for old standard: {self.scale}")