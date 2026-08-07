"""Veridic native dimensional algebra."""

from .model import Dimension, Exponent

DIMENSIONLESS = Dimension.dimensionless()

TIME = Dimension.base("Time")
LENGTH = Dimension.base("Length")
MASS = Dimension.base("Mass")
TEMPERATURE = Dimension.base("Temperature")
DATA = Dimension.base("Data")
COUNT = Dimension.base("Count")
ANGLE = Dimension.base("Angle")

__all__ = [
    "ANGLE",
    "COUNT",
    "DATA",
    "DIMENSIONLESS",
    "LENGTH",
    "MASS",
    "TEMPERATURE",
    "TIME",
    "Dimension",
    "Exponent",
]
