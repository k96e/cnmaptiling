from typing import Union, Type

class Angle:
    def __init__(self, d: int = 0, m: int = 0, s: float = 0) -> None:
        self.degrees: int = d
        self.minutes: int = m
        self.seconds: float = s
        self._normalize()
    
    @classmethod
    def from_decimal(cls: Type['Angle'], decimal_degrees: float) -> 'Angle':
        degrees = int(decimal_degrees)
        decimal_minutes = (decimal_degrees - degrees) * 60
        minutes = int(decimal_minutes)
        seconds = (decimal_minutes - minutes) * 60
        res = cls(degrees, minutes, seconds)
        res._normalize()
        return res
    
    def _normalize(self) -> None:
        if abs(self.seconds - 60) < 1e-10:
            self.seconds = 0
            self.minutes += 1
            
        additional_minutes, self.seconds = divmod(self.seconds, 60)
        self.minutes += additional_minutes
        
        if abs(self.minutes - 60) < 1e-10:
            self.minutes = 0
            self.degrees += 1
            
        additional_degrees, self.minutes = divmod(self.minutes, 60)
        self.degrees += additional_degrees
        
        self.degrees = self.degrees % 360
        self.minutes = int(self.minutes)
        self.degrees = int(self.degrees)
    
    def to_decimal(self) -> float:
        return self.degrees + self.minutes / 60 + self.seconds / 3600
    
    def __truediv__(self, other: Union['Angle', int, float]) -> Union[float, 'Angle']:
        if isinstance(other, Angle):
            return self.to_decimal() / other.to_decimal()
        else:
            return Angle.from_decimal(self.to_decimal() / other)
    
    def __mod__(self, other: Union['Angle', int, float]) -> 'Angle':
        if isinstance(other, Angle):
            return Angle.from_decimal(self.to_decimal() % other.to_decimal())
        else:
            return Angle.from_decimal(self.to_decimal() % other)
    
    def __add__(self, other: Union['Angle', int, float]) -> 'Angle':
        if isinstance(other, Angle):
            return Angle.from_decimal(self.to_decimal() + other.to_decimal())
        else:
            return Angle.from_decimal(self.to_decimal() + other)
        
    def __mul__(self, other: Union[int, float]) -> 'Angle':
        return Angle.from_decimal(self.to_decimal() * other)

    def __str__(self) -> str:
        return f"{self.degrees}° {self.minutes}' {self.seconds:.3f}\""
    
    def __repr__(self) -> str:
        return f"Angle({self.degrees}° {self.minutes}' {self.seconds:.3f}\")"