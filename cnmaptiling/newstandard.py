from .angle import Angle
from .scale import Scale
from math import floor

class NewStandard():
    """
    国家标准比例尺地形图新图号
    """
    def __init__(self, scale: Scale = None):
        self.scale = scale
        
    def latlon_to_newstandard(self, lon: Angle, lat: Angle) -> str:
        """
        将经纬度转换为新图号
        """
        if self.scale is None:
            raise ValueError("Scale must be set for latlon_to_newstandard")
        a = floor(lat/Angle(d=4)) + 1
        a_char = chr(a + 64)
        b = floor(lon/Angle(d=6)) + 31
        c = floor(Scale.LEVEL_1M.lat_diff/self.scale.lat_diff) - floor((lat%Scale.LEVEL_1M.lat_diff)/self.scale.lat_diff)
        d = floor((lon%Scale.LEVEL_1M.lon_diff)/self.scale.lon_diff) + 1
        if self.scale in [Scale.LEVEL_1K, Scale.LEVEL_500]:
            return f"{a_char}{b:02d}{self.scale.code}{c:04d}{d:04d}"
        if self.scale == Scale.LEVEL_1M:
            return f"{a_char}{b:02d}"
        return f"{a_char}{b:02d}{self.scale.code}{c:03d}{d:03d}"

    def newstandard_to_latlon(self, new_standard_number: str) -> tuple[tuple[Angle, Angle], tuple[Angle, Angle]]:
        """
        将新图号转换为经纬度范围
        """
        a = ord(new_standard_number[0]) - 64
        b = int(new_standard_number[1:3])
        scale_code = new_standard_number[3]
        scale = Scale.from_code(scale_code)
        c = int(new_standard_number[4:8]) if scale in [Scale.LEVEL_1K, Scale.LEVEL_500] else int(new_standard_number[4:7])
        d = int(new_standard_number[8:12]) if scale in [Scale.LEVEL_1K, Scale.LEVEL_500] else int(new_standard_number[7:10])
        lon = Scale.LEVEL_1M.lon_diff * (b-31) + scale.lon_diff * (d-1)
        lat = Scale.LEVEL_1M.lat_diff * (a-1) + scale.lat_diff * (Scale.LEVEL_1M.lat_diff/scale.lat_diff - c)
        lon_ne = lon + scale.lon_diff
        lat_ne = lat + scale.lat_diff
        return (lon, lat), (lon_ne, lat_ne)