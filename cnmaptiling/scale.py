from enum import Enum

from .angle import Angle

class Scale(Enum):
    """
    Enum for scale levels.
    (code, longitude diff, latitude diff, map nums)
    """
    LEVEL_1M = ("A", Angle(d=6), Angle(d=4), 1) # 1:1,000,000
    LEVEL_500K = ("B", Angle(d=3), Angle(d=2), 2) # 1:500,000
    LEVEL_250K = ("C", Angle(d=1,m=30), Angle(d=1), 4) # 1:250,000
    LEVEL_100K = ("D", Angle(m=30), Angle(m=20), 12) # 1:100,000
    LEVEL_50K = ("E", Angle(m=15), Angle(m=10), 2) # 1:50,000
    LEVEL_25K = ("F", Angle(m=7,s=30), Angle(m=5), 2) # 1:25,000
    LEVEL_10K = ("G", Angle(m=3,s=45), Angle(m=2,s=30), 8) # 1:10,000
    LEVEL_5K = ("H", Angle(m=1,s=52.5), Angle(m=1,s=15), 2) # 1:5,000
    LEVEL_2K = ("I", Angle(s=37.5), Angle(s=25), 0) # 1:2,000
    LEVEL_1K = ("J", Angle(s=18.75), Angle(s=12.5), 0) # 1:1,000
    LEVEL_500 = ("K", Angle(s=9.375), Angle(s=6.25), 0) # 1:500

    @classmethod
    def from_code(cls, code: str) -> 'Scale':
        """
        Get Scale from code.
        """
        code = code.upper()
        for scale in cls:
            if scale.code == code:
                return scale
        raise ValueError(f"Invalid scale code: {code}")

    def __init__(self, code: str, lon_diff: Angle, lat_diff: Angle, nums: int) -> None:
        self.code = code
        self.lon_diff = lon_diff
        self.lat_diff = lat_diff
        self.nums = nums
