import math
import logging
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.lib.function_base import angle
from numpy import sin, cos, pi, linspace

logger = logging.getLogger(__name__)


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


def validate_filling(h: int | float, d: int | float) -> bool:
    """
    If the pipe filling height is greater than the pipe dimension is correct.
    If not return False otherwise, return True

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]

    Return:
        bool: Are the given values correct.
    """
    if h > d:
        logger.info(f"h cannot be greater than d.")
        return False
    return True


def calc_f(h: int | float, d: int | float) -> int | float:
    """
    Calculate the cross-sectional area of a pipe.
    Given its pipe filling height and diameter of pipe.

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]

    Return:
        area (int, float): cross-sectional area of the wetted part of the pipe [m2]
    """
    if validate_filling(h, d):
        radius = d / 2
        chord = math.sqrt((radius ** 2 - ((h - radius) ** 2))) * 2
        alpha = math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))
        if h > radius:
            return pi * radius ** 2 - (1 / 2 * (alpha - math.sin(alpha)) * radius ** 2)
        elif h == radius:
            return pi * radius ** 2 / 2
        elif h == d:
            return pi * radius ** 2
        else:
            return 1 / 2 * (alpha - math.sin(alpha)) * radius ** 2


def calc_filling_percentage(h: int | float, d: int | float) -> int | float:
    """
    Calculate the percentage value of pipe filling height.

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]

    Return:
        filled height (int, float): percentage of pipe that is filled with water.
    """
    return (h / d) * 100


def calc_u(h: int | float, d: int | float) -> int | float:
    """
    Calculate the circumference of a wetted part of pipe

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]

    Return:
        circumference (int, float): circumference of a wetted part of pipe
    """
    if validate_filling(h, d):
        radius = d / 2
        chord = math.sqrt((radius ** 2 - (h-radius) ** 2)) * 2
        alpha = math.degrees(math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2)))
        if h > radius:
            return 2 * math.pi * radius - (alpha / 360 * 2 * math.pi * radius)
        return alpha / 360 * 2 * math.pi * radius


def calc_rh(h: int | float, d: int | float) -> int | float:
    """
    Calculate the hydraulic radius Rh, i.e. the ratio of the cross-section f
    to the contact length of the sewage with the sewer wall, called the wetted circuit U.

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]

    Return:
        Rh (int, float): hydraulic radius [m]
    """
    try:
        return calc_f(h, d) / calc_u(h, d)
    except ZeroDivisionError:
        return 0


def calc_velocity(h: int | float, d: int | float, i: int | float) -> int | float:
    """
    Calculate the speed of the sewage flow in the sewer.

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]
        i (int, float): fall in the bottom of the sewer [‰]

    Return:
        v (int, float): sewage flow velocity in the sewer [m/s]
    """
    i = i / 1000
    if validate_filling(h, d):
        return 1 / 0.013 * calc_rh(h, d) ** (2/3) * i ** 0.5


def calc_flow(h: int | float, d: int | float, i: int | float) -> int | float:
    """
    Calculate sewage flow in the channel

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]
        i (int, float): fall in the bottom of the sewer [‰]

    Return:
        q (int, float): sewage flow in the channel [dm3/s]
    """
    if validate_filling(h, d):
        f = calc_f(h, d)
        v = calc_velocity(h, d, i)
        return f * 1000 * v


def min_slope(h, d):
    """Rh(h) — promień hydrauliczny w [mm]."""
    rh = calc_rh(h, d)
    return 0.25 / rh


def max_slope(h, d):
    pass


def max_h(d):
    if 0.2 <= d <= 0.3:
        return 0.6 * d
    elif 0.3 < d <= 0.5:
        return 0.7 * d
    elif 0.5 < d <= 0.9:
        return 0.75 * d
    elif 0.9 < d:
        return 0.8 * d


def calc_h(q, d, i):
    h = 0
    flow = 0
    while flow < q:
        if validate_filling(h, d):
            flow = calc_flow(h, d, i)
            h += 0.0001
    return h


def draw_pipe_section(h, d, max_filling=None):
    if max_filling is None:
        max_filling = d
    if validate_filling(h, d):
        radius = d / 2
        # draw center point  - 0, 0
        plt.plot(0, 0, color='black', marker='o')
        plt.gca().annotate('O (0, 0)', xy=(0 + radius / 10, 0 + radius / 10), xycoords='data', fontsize=12)
        plt.xlim(-radius - 0.05, radius + 0.05)
        plt.ylim(-radius, radius + 0.07)
        plt.gca().set_aspect('equal')

        # draw circle
        angels = linspace(0 * pi, 2 * pi, 100)
        xs = radius * cos(angels)
        ys = radius * sin(angels)
        # add circle
        plt.plot(xs, ys, color='brown', label=f"Pipe: DN {d} [m]")

        # draw diameter
        plt.plot(radius, 0, marker='o', color='blue')
        plt.plot(-radius, 0, marker='o', color='blue')
        plt.plot([radius, -radius], [0, 0])
        # annotation to diameter
        plt.gca().annotate(f"Diameter={d}", xy=(radius / 8, -radius / 5), xycoords='data', fontsize=12)

        # draw level of water
        plt.plot(0, -radius, marker='o', color='purple')
        plt.plot(0, h - radius, marker='o', color='purple')
        plt.plot([0, 0], [-radius, h - radius], color='purple', label=f'Pipe filling height: {h} [m]')
        plt.gca().annotate(f"Water lvl={h}", xy=(radius / 2, h - radius + 0.01), xycoords='data', fontsize=12)

        # Draw arc as created by water level
        chord = math.sqrt((radius ** 2 - ((h - radius) ** 2))) * 2
        alpha = math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))

        if h > max_filling:
            color = 'red'
        else:
            color = 'blue'
        # Create arc
        if h <= radius:
            diff = math.radians(180) - alpha
            arc_angles = linspace(diff / 2, alpha + diff / 2, 20)
        else:
            diff = math.radians(180) - alpha
            arc_angles = linspace(-diff / 2, alpha + diff + diff / 2, 100)
        arc_xs = radius * cos(arc_angles)
        arc_ys = radius * sin(arc_angles)
        plt.plot(arc_xs, -arc_ys, color=color, lw=3)
        plt.plot([-arc_xs[0], -arc_xs[-1]], [-arc_ys[0], -arc_ys[-1]],  marker='o', color=color, lw=3, label=f"Wetted part of pipe: {calc_f(h, d):.2f} [m2]")
        plt.grid(True)
        plt.legend(loc='upper left')
        plt.show()
    else:
        logger.info(f"h cannot be greater than d.")
















