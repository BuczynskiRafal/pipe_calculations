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
        filled area (int, float): percentage of pipe that is filled with water.
    """
    return (calc_f(h, d) / (pi * (d / 2) ** 2)) * 100


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


def calc_rh(f: int | float, u: int | float) -> int | float:
    """
    Calculate the hydraulic radius Rh, i.e. the ratio of the cross-section f
    to the contact length of the sewage with the sewer wall, called the wetted circuit U.

    Args:
        f (int, float): cross-sectional area of the wetted part of the pipe [m2]
        u (int, float): circumference of a wetted part of pipe [m]

    Return:
        Rh (int, float): hydraulic radius [m]
    """
    try:
        return f / u
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
        f = calc_f(h, d)
        u = calc_u(h, d)
        rh = calc_rh(f, u)
        return 1 / 0.013 * rh ** (2/3) * i ** 0.5


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
    f = calc_f(h, d)
    u = calc_u(h, d)
    rh = calc_rh(f, u)
    return 1 / (4 * rh)


def max_slope(h, d):
    """Rh(h) — promień hydrauliczny w [cm]."""
    f = calc_f(h, d)
    u = calc_u(h, d)
    rh = calc_rh(f, u)
    return 1 / (4 * rh)


def find_h(q, d, i):
    h = 0
    flow = 0
    while flow <= q:
        if validate_filling(h, d):
            flow = calc_flow(h, d, i)
            h += 0.001
            print(f"q: {q}, flow: {flow:.4f}, h: {h:.4f}")
    return h


def draw_pipe_section(h, d):
    if validate_filling(h, d):
        radius = d / 2
        # draw center point  - 0, 0
        plt.plot(0, 0, color='black', marker='o')
        plt.gca().annotate('O (0, 0)', xy=(0 + radius / 10, 0 + radius / 10), xycoords='data', fontsize=12)
        plt.xlim(-radius - 0.05, radius + 0.05)
        plt.ylim(-radius, radius + 0.05)
        # ustawia podziałkę na osiach
        plt.gca().set_aspect('equal')

        # draw circle
        angels = linspace(0 * pi, 2 * pi, 100)
        xs = radius * cos(angels)
        ys = radius * sin(angels)
        # add circle
        plt.plot(xs, ys, color='brown')

        # draw diameter
        plt.plot(radius, 0, marker='o', color='blue')
        plt.plot(-radius, 0, marker='o', color='blue')
        plt.plot([radius, -radius], [0, 0])
        # annotation to diameter
        plt.gca().annotate(f"Diameter={d}", xy=(radius / 8, -radius / 5), xycoords='data', fontsize=12)

        # draw level of water
        plt.plot(0, -radius, marker='o', color='purple')
        plt.plot(0, h - radius, marker='o', color='purple')
        plt.plot([0, 0], [-radius, h - radius], color='purple')
        plt.gca().annotate(f"Water lvl={h}", xy=(radius / 2, h - radius + 0.01), xycoords='data', fontsize=12)

        # Draw arc as created by water level
        # cięciwa - długość
        chord = math.sqrt((radius ** 2 - ((h - radius) ** 2))) * 2

        # calculate angle - kąt obliczany z reguły cosinusów
        alpha = math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))

        # Create arc
        if h <= radius:
            diff = math.radians(180) - alpha
            arc_angles = linspace(diff / 2, alpha + diff / 2, 20)
            # arc_xs = radius * cos(arc_angles)
            # arc_ys = radius * sin(arc_angles)
            # plt.plot(arc_xs, -arc_ys, color='red', lw=3)
        else:
            diff = math.radians(180) - alpha
            arc_angles = linspace(-diff / 2, alpha + diff + diff / 2, 100)
            # print(arc_angles)
        arc_xs = radius * cos(arc_angles)
        arc_ys = radius * sin(arc_angles)
        plt.plot(arc_xs, -arc_ys, color='blue', lw=3)
        plt.plot([-arc_xs[0], -arc_xs[-1]], [-arc_ys[0], -arc_ys[-1]],  marker='o', color='blue', lw=3)
        plt.show()
    else:
        logger.info(f"h cannot be greater than d.")


def prepare_calculations_and_chart(h: int | float, d: int | float, i: int | float) -> None:
    v = calc_velocity(h, d, i)
    q = calc_flow(h, d, i)
    fill = calc_filling_percentage(h, d)
    draw_pipe_section(h, d)

print(calc_velocity(0.08, 0.2, 20))
print(calc_flow(0.08, 0.2, 20))
print(calc_filling_percentage(0.08, 0.2))
print(draw_pipe_section(0.08, 0.2))


def calc_h(q, d, i):
    pass


def insert_excel_data(path):
    data = pd.read_excel(path)
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_excel_pipe_settings(path):
    data = pd.read_excel(path)
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_csv_data(path):
    data = pd.read_csv(path, encoding='unicode_escape')
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_excel_pipe_settings_from_cloud(path):
    response = requests.get(path)
    local_pipe_settings = 'pipe_settings.xlsx'
    with open(local_pipe_settings, 'wb') as file:
        file.write(response.content)
    data = pd.read_excel(local_pipe_settings)
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


def insert_csv_pipe_settings(path):
    data = pd.read_csv(path, encoding='unicode_escape')
    df = pd.DataFrame(data)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df
















