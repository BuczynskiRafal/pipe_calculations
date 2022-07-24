import math
import numpy as np


class PipeSettings:
    def __init__(self, diameter, min_slope, max_slope, max_filling=0.9, max_velocity=3):
        self.diameter = diameter
        self.min_slope = 1 / self.diameter
        self.max_slope = max_slope
        self.max_filling = max_filling  # napełnienie kanału
        self.max_velocity = max_velocity


class Pipe:
    def __init__(self):
        self.pipe = [
            PipeSettings(0.16, 1, 20),
            PipeSettings(0.2, 1, 20),
            PipeSettings(0.25, 1, 20),
            PipeSettings(0.315, 1, 20),
            PipeSettings(0.4, 1, 20),
            PipeSettings(0.5, 1, 20),
        ]


def calc_cross_sectional_area(h, d):
    """
    This function calculates the cross-sectional area of a cylinder given its height and diameter

    :param h: napełnienie [m]
    :param d: diameter of the pipe [m]
    """
    # promień
    radius = d / 2

    # cięciwa
    chord = math.sqrt((radius ** 2 - ((h-radius) ** 2))) * 2

    # calculate angle - kąt obliczany z reguły cosinusów
    alpha = math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))

    if h > radius:
        return math.pi * radius ** 2 - (1 / 2 * (alpha - math.sin(alpha)) * radius ** 2)
    elif h == radius:
        return math.pi * radius ** 2 / 2
    else:
        return 1 / 2 * (alpha - math.sin(alpha)) * radius ** 2


def calc_filling_percentage(h, d):
    return calc_cross_sectional_area(h, d) / (math.pi * (d / 2) ** 2) * 100


def calc_u(h, d):
    radius = d / 2
    # cięciwa
    chord = math.sqrt((radius ** 2 - (h-radius) ** 2)) * 2
    angle = math.degrees(math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2)))
    return angle / 360 * 2 * math.pi * radius


def calc_rh(f, u):
    return f / u


def calc_velocity(h, d, i):
    """
    This function takes three arguments, `c`, `rh`, and `i`, and returns the velocity of water inside pipe.

    :param c: coefficient calculated according to Manning's formula
    :param rh: hydraulic radius, equal to the ratio of the cross-sectional area to the wetted circumference [m]
    :param i: decrease of the wastewater table, equal to the slope of the bottom of the sewer when the liquid flows with a free mirror, or the decrease of the pressure line when the sewer works under pressure,
    :return: The velocity of the wave.
    """
    f = calc_cross_sectional_area(h, d)
    u = calc_u(h, d)
    return (1 / 0.013) * (calc_rh(f, u) ** (2/3)) * i ** (1/2)


def calc_flow(h, d, i):
    """
    This function takes in a flow rate and a velocity and returns the product of the two

    :param f:  powierzchni przekroju, którym płyną ścieki, tzw. przekroju czynnego f, charakteryzowanego napełnieniem h i średnicą przewodu D,
    :param v: the velocity of the fluid
    :return: The product of f and v
    """
    f = calc_cross_sectional_area(h, d)
    v = calc_velocity(h, d, i)
    return f * v

# mam podany przepływ i spadek, chcę sprawdzić czy dobrano poprawnie średnicę
# ma zwrócić minimalną średnicę
def validate_diameter(q, d, i):
    # d - dobrana średnica
    # q - aktualny przepływ
    # i - dobrany spadek

    # 1 sprawdzić napełnienie kanału. - obliczyć h na podstawie przepływu średnicy i spadku
    # 1 oblicz prędkość wody
    v = calc_velocity()


























