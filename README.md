# cnmaptiling

国家基本比例尺地形图分幅和编号的Python实现，支持新旧规范坐标到图号以及图号到图廓范围计算。

## 安装
``` bash
pip install cnmaptiling
```

## 使用

``` python
from cnmaptiling import Angle, Scale, NewStandard, OldStandard

# 经纬度
lat = Angle(d=31, m=50, s=57)
lon = Angle(d=117, m=17, s=24)

# 新图号
print(NewStandard(Scale.LEVEL_1M).latlon_to_newstandard(lon, lat))
print(NewStandard(Scale.LEVEL_50K).latlon_to_newstandard(lon, lat))
# H50
# H50E001014

# 新图号图廓范围
print(NewStandard().newstandard_to_latlon("H50E001014"))
# ((Angle(117° 15' 0.000"), Angle(31° 50' 0.000")), (Angle(117° 30' 0.000"), Angle(32° 0' 0.000")))

# 旧图号
print(OldStandard(Scale.LEVEL_1M).latlon_to_oldstandard(lon, lat))
print(OldStandard(Scale.LEVEL_50K).latlon_to_oldstandard(lon, lat))
# H-50
# H-50-7-B

# 旧图号图廓范围
print(OldStandard(Scale.LEVEL_50K).oldstandard_to_latlon("H-50-7-B"))
# ((Angle(117° 15' 0.000"), Angle(31° 50' 0.000")), (Angle(117° 30' 0.000"), Angle(32° 0' 0.000")))
```

## 参考
GB/T 13989-2012 国家基本比例尺地形图分幅和编号\
王家耀.地图学原理与方法\
高井祥.数字地形测量学 