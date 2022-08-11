import math
import logging
import matplotlib.pyplot as plt
import pandas as pd
from numpy import sin, cos, pi, linspace

logger = logging.getLogger(__name__)


class CircularSectionPipe:
    def __init__(self, diameter, flow, slope, h=None):
        self._diameter = diameter
        self.flow = flow
        self.h = h
        self.slope = slope
        self.min_slope = self.min_slope()
        self.max_slope = max_slope
        self.max_filling = max_filling  # napełnienie kanału
        self.max_velocity = max_velocit

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, value):
        if isinstance(value, str):
            value = float(value)
        if isinstance(value, (int, float)) and value in (0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0):
            self.diameter = value

    @diameter.deleter
    def diameter(self):
        del self.diameter

    @property
    def h(self):
        return self.h

    @h.setter
    def h(self, value):
        if value is not None and value <= self.diameter:
            self.h = value
        else:
            self.h = CircularSectionPipe.calc_h(self)

    @h.deleter
    def h(self):
        del self.h

    def calc_f(self) -> float:
        """
        Calculate the cross-sectional area of a pipe.
        Given its pipe filling height and diameter of pipe.

        Return:
            area (int, float): cross-sectional area of the wetted part of the pipe [m2]
        """
        radius = self.diameter / 2
        chord = math.sqrt((radius ** 2 - ((self.h - radius) ** 2))) * 2
        alpha = math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))
        if self.h > radius:
            return pi * radius ** 2 - (1 / 2 * (alpha - math.sin(alpha)) * radius ** 2)
        elif self.h == radius:
            return pi * radius ** 2 / 2
        elif self.h == self.diameter:
            return pi * radius ** 2
        else:
            return 1 / 2 * (alpha - math.sin(alpha)) * radius ** 2

    def calc_filling_percentage(self) -> float:
        """
        Calculate the percentage value of pipe filling height.

        Return:
            filled height (int, float): percentage of pipe that is filled with water.
        """
        return (self.h / self.diameter) * 100

    def calc_u(self) -> float:
        """
        Calculate the circumference of a wetted part of pipe

        Return:
            circumference (int, float): circumference of a wetted part of pipe
        """
        radius = self.diameter / 2
        chord = math.sqrt((radius ** 2 - (self.h - radius) ** 2)) * 2
        alpha = math.degrees(
            math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))
        )
        if self.h > radius:
            return 2 * math.pi * radius - (alpha / 360 * 2 * math.pi * radius)
        return alpha / 360 * 2 * math.pi * radius

    def calc_rh(self) -> float:
        """
        Calculate the hydraulic radius Rh, i.e. the ratio of the cross-section f
        to the contact length of the sewage with the sewer wall, called the wetted circuit U.

        Return:
            Rh (int, float): hydraulic radius [m]
        """
        try:
            return self.calc_f() / self.calc_u()
        except ZeroDivisionError:
            return 0

    def calc_velocity(self) -> float:
        """
        Calculate the speed of the sewage flow in the sewer.

        Return:
            v (int, float): sewage flow velocity in the sewer [m/s]
        """
        i = self.slope / 1000
        return 1 / 0.013 * self.calc_rh() ** (2 / 3) * i**0.5

    def calc_flow(self) -> float:
        """
        Calculate sewage flow in the channel

        Return:
            q (int, float): sewage flow in the channel [dm3/s]
        """
        f = self.calc_f()
        v = self.calc_velocity()
        return f * 1000 * v

    def calc_h(self):
        h = 0
        q = 0
        while q < self.flow:
            if h <= self.diameter:
                q = self.calc_flow()
                h += 0.0001
        return self.h(h)

    def min_slope(self):
        """
        If the pipe  filling is greater than 0.3, then the minimum slope is 1/d, otherwise it's 0.25/rh

        Return:
            i (int, float): The minimum slope of the channel [‰]
        """
        if self.h / self.diameter >= 0.3:
            return 1 / self.diameter
        else:
            return 0.25 / self.calc_rh()

    def max_slope(self, d, v=5):
        """
        Maximum slopes of the channel bottom calculated according to the Manning formula.
        The maximum slopes (imax) of the channel bottom were determined (according to WTP)
        in a similar way, i.e. with complete filling, the sewage flow velocity should not exceed the value of

            Vmax = 3.0 m / s -  in household and industrial sewers for concrete and ceramic pipes,
            Vmax = 5.0 m / s -  in household and industrial sewers for reinforced concrete and cast iron pipes,
            Vmax = 7.0 m / s -  in rainwater and combined sewers, regardless of the sewer material, as such sewers,
                                with a significant filling, operate periodically, compared to household and industrial
                                sewers.

        Args:
            d (int, float): pipe diameter [m]
            v (int):        max sewage flow velocity in the sewer [m/s]

        Return:
            i (int, float): The maximum slope of the channel [‰]
        """
        slopes = {
            'DN': [0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2],
            3: [82.8, 60.3, 47.7, 32.4, 24.3, 18.9, 13.5, 9.9, 5.6, 3.8],
            5: [230, 167.5, 132.5, 90, 67.5, 52.5, 37.5, 27.5, 15.6, 10.6],
            7: [450.8, 328.3, 259.7, 176.4, 132.3, 102.9, 73.5, 53.9, 30.6, 20.9],
        }
        df = pd.DataFrame(data=slopes)
        val = df.loc[df['DN'] == d][v]
        return float(val)

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
            plt.plot(0, 0, color="black", marker="o")
            plt.gca().annotate(
                "O (0, 0)",
                xy=(0 + radius / 10, 0 + radius / 10),
                xycoords="data",
                fontsize=12,
            )
            plt.xlim(-radius - 0.05, radius + 0.05)
            plt.ylim(-radius, radius + 0.07)
            plt.gca().set_aspect("equal")

            # draw circle
            angels = linspace(0 * pi, 2 * pi, 100)
            xs = radius * cos(angels)
            ys = radius * sin(angels)
            # add circle
            plt.plot(xs, ys, color="brown", label=f"Pipe: DN {d} [m]")

            # draw diameter
            plt.plot(radius, 0, marker="o", color="blue")
            plt.plot(-radius, 0, marker="o", color="blue")
            plt.plot([radius, -radius], [0, 0])
            # annotation to diameter
            plt.gca().annotate(
                f"Diameter={d}", xy=(radius / 8, -radius / 5), xycoords="data", fontsize=12
            )

            # draw level of water
            plt.plot(0, -radius, marker="o", color="purple")
            plt.plot(0, h - radius, marker="o", color="purple")
            plt.plot(
                [0, 0],
                [-radius, h - radius],
                color="purple",
                label=f"Pipe filling height: {h} [m]",
            )
            plt.gca().annotate(
                f"Water lvl={h}",
                xy=(radius / 2, h - radius + 0.01),
                xycoords="data",
                fontsize=12,
            )

            # Draw arc as created by water level
            chord = math.sqrt((radius ** 2 - ((h - radius) ** 2))) * 2
            alpha = math.acos((radius ** 2 + radius ** 2 - chord ** 2) / (2 * radius ** 2))

            if h > max_filling:
                color = "red"
            else:
                color = "blue"
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
            plt.plot(
                [-arc_xs[0], -arc_xs[-1]],
                [-arc_ys[0], -arc_ys[-1]],
                marker="o",
                color=color,
                lw=3,
                label=f"Wetted part of pipe: {calc_f(h, d):.2f} [m2]",
            )
            plt.grid(True)
            plt.legend(loc="upper left")
            plt.show()
        else:
            logger.info(f"h cannot be greater than d.")


def validate_filling(h: float, d: float) -> bool:
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


def calc_f(h: float, d: float) -> float:
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
        chord = math.sqrt((radius**2 - ((h - radius) ** 2))) * 2
        alpha = math.acos((radius**2 + radius**2 - chord**2) / (2 * radius**2))
        if h > radius:
            return pi * radius**2 - (1 / 2 * (alpha - math.sin(alpha)) * radius**2)
        elif h == radius:
            return pi * radius**2 / 2
        elif h == d:
            return pi * radius**2
        else:
            return 1 / 2 * (alpha - math.sin(alpha)) * radius**2


def calc_filling_percentage(h: float, d: float) -> float:
    """
    Calculate the percentage value of pipe filling height.

    Args:
        h (int, float): pipe filling height [m]
        d (int, float): pipe diameter [m]

    Return:
        filled height (int, float): percentage of pipe that is filled with water.
    """
    return (h / d) * 100


def calc_u(h: float, d: float) -> float:
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
        chord = math.sqrt((radius**2 - (h - radius) ** 2)) * 2
        alpha = math.degrees(
            math.acos((radius**2 + radius**2 - chord**2) / (2 * radius**2))
        )
        if h > radius:
            return 2 * math.pi * radius - (alpha / 360 * 2 * math.pi * radius)
        return alpha / 360 * 2 * math.pi * radius


def calc_rh(h: float, d: float) -> float:
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


def calc_velocity(h: float, d: float, i: float) -> float:
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
        return 1 / 0.013 * calc_rh(h, d) ** (2 / 3) * i**0.5


def calc_flow(h: float, d: float, i: float) -> float:
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
    """
    If the pipe  filling is greater than 0.3, then the minimum slope is 1/d, otherwise it's 0.25/rh

    Args:
        h (int, float): pipe filling height in circular section [m]
        d (int, float): pipe diameter [m]

    Return:
        i (int, float): The minimum slope of the channel [‰]
    """
    if h / d >= 0.3:
        return 1 / d
    else:
        return 0.25 / calc_rh(h, d)

# not only for circular section
# def min_slope(h, d, section='circular', f=None, rh=None):
#     """
#     The minimum slope of a circular pipe is 1/d if ,
#     and the minimum slope of a non-circular pipe is 0.25/rh
#
#     Args:
#         h (int, float): pipe filling height in circular section [m]
#         d (int, float): pipe diameter [m]
#         section (str): the shape of the cross-section of the channel, defaults to circular (optional)
#         f (int, float): shape factor. Default None, is needed to calculate 'rectangular', 'trapezoidal', 'pentagonal', 'complex' section pipes.
#         rh (int, float): hydraulic radius [m]. If section is circular use calc_rh to calculate input rh.
#
#     Return:
#         i (int, float): The minimum slope of the channel [‰]
#     """
#     if h / d >= 0.3:
#         if section == 'circular':
#             return 1 / d
#     elif section in ['circular', 'circular worn out', 'egg', 'pear', 'bell']:
#         return 0.25 / rh
#     elif section in ['rectangular', 'trapezoidal', 'pentagonal', 'complex']:
#         return 0.25 / f * rh


def max_slope(d, v=5):
    """
    Maximum slopes of the channel bottom calculated according to the Manning formula.
    The maximum slopes (imax) of the channel bottom were determined (according to WTP)
    in a similar way, i.e. with complete filling, the sewage flow velocity should not exceed the value of

        Vmax = 3.0 m / s -  in household and industrial sewers for concrete and ceramic pipes,
        Vmax = 5.0 m / s -  in household and industrial sewers for reinforced concrete and cast iron pipes,
        Vmax = 7.0 m / s -  in rainwater and combined sewers, regardless of the sewer material, as such sewers,
                            with a significant filling, operate periodically, compared to household and industrial
                            sewers.

    Args:
        d (int, float): pipe diameter [m]
        v (int):        max sewage flow velocity in the sewer [m/s]

    Return:
        i (int, float): The maximum slope of the channel [‰]
    """
    slopes = {
        'DN': [0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2],
        3: [82.8, 60.3, 47.7, 32.4, 24.3, 18.9, 13.5, 9.9, 5.6, 3.8],
        5: [230, 167.5, 132.5, 90, 67.5, 52.5, 37.5, 27.5, 15.6, 10.6],
        7: [450.8, 328.3, 259.7, 176.4, 132.3, 102.9, 73.5, 53.9, 30.6, 20.9],
    }
    df = pd.DataFrame(data=slopes)
    val = df.loc[df['DN'] == d][v]
    return float(val)


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
        plt.plot(0, 0, color="black", marker="o")
        plt.gca().annotate(
            "O (0, 0)",
            xy=(0 + radius / 10, 0 + radius / 10),
            xycoords="data",
            fontsize=12,
        )
        plt.xlim(-radius - 0.05, radius + 0.05)
        plt.ylim(-radius, radius + 0.07)
        plt.gca().set_aspect("equal")

        # draw circle
        angels = linspace(0 * pi, 2 * pi, 100)
        xs = radius * cos(angels)
        ys = radius * sin(angels)
        # add circle
        plt.plot(xs, ys, color="brown", label=f"Pipe: DN {d} [m]")

        # draw diameter
        plt.plot(radius, 0, marker="o", color="blue")
        plt.plot(-radius, 0, marker="o", color="blue")
        plt.plot([radius, -radius], [0, 0])
        # annotation to diameter
        plt.gca().annotate(
            f"Diameter={d}", xy=(radius / 8, -radius / 5), xycoords="data", fontsize=12
        )

        # draw level of water
        plt.plot(0, -radius, marker="o", color="purple")
        plt.plot(0, h - radius, marker="o", color="purple")
        plt.plot(
            [0, 0],
            [-radius, h - radius],
            color="purple",
            label=f"Pipe filling height: {h} [m]",
        )
        plt.gca().annotate(
            f"Water lvl={h}",
            xy=(radius / 2, h - radius + 0.01),
            xycoords="data",
            fontsize=12,
        )

        # Draw arc as created by water level
        chord = math.sqrt((radius**2 - ((h - radius) ** 2))) * 2
        alpha = math.acos((radius**2 + radius**2 - chord**2) / (2 * radius**2))

        if h > max_filling:
            color = "red"
        else:
            color = "blue"
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
        plt.plot(
            [-arc_xs[0], -arc_xs[-1]],
            [-arc_ys[0], -arc_ys[-1]],
            marker="o",
            color=color,
            lw=3,
            label=f"Wetted part of pipe: {calc_f(h, d):.2f} [m2]",
        )
        plt.grid(True)
        plt.legend(loc="upper left")
        plt.show()
    else:
        logger.info(f"h cannot be greater than d.")
