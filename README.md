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
lat = Angle(d=39, m=54, s=30)
lon = Angle(d=116, m=28, s=15)

# 新图号
print(NewStandard(Scale.LEVEL_1M).latlon_to_newstandard(lon, lat))
print(NewStandard(Scale.LEVEL_50K).latlon_to_newstandard(lon, lat))
# J50
# J50E001010

# 新图号图廓范围
print(NewStandard().newstandard_to_latlon("J50E001010"))
# ((Angle(116° 15' 0.000"), Angle(39° 50' 0.000")), (Angle(116° 30' 0.000"), Angle(40° 0' 0.000")))

# 旧图号
print(OldStandard(Scale.LEVEL_1M).latlon_to_oldstandard(lon, lat))
print(OldStandard(Scale.LEVEL_50K).latlon_to_oldstandard(lon, lat))
# J-50
# J-50-5-B

# 旧图号图廓范围
print(OldStandard(Scale.LEVEL_50K).oldstandard_to_latlon("J-50-5-B"))
# ((Angle(116° 15' 0.000"), Angle(39° 50' 0.000")), (Angle(116° 30' 0.000"), Angle(40° 0' 0.000")))
```

## 参考
GB/T 13989-2012 国家基本比例尺地形图分幅和编号\
王家耀.地图学原理与方法\
高井祥.数字地形测量学 