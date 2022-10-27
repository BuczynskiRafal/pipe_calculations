import pandas as pd
import numpy as np
from pyswmm import Simulation, Subcatchments


def get_runoff(min_slope=0.05, max_slope=100, file_path='example.inp'):
    slope = []
    runoff = []
    s = min_slope
    while s < max_slope:
        slope.append(s)
        with Simulation(file_path) as sim:
            s1 = Subcatchments(sim)["S2"]
            s1.slope = s

            max_runoff = 0
            # Where your simulation runs
            for step in sim:
                if s1.runoff > max_runoff:
                    max_runoff = s1.runoff
            runoff.append(max_runoff)
            # print("For Slope: {}, max runoff is {}".format(slope, max_runoff))
        s += 0.05
    return {"slope": slope, "runoff": runoff}

data = get_runoff()

df = pd.DataFrame(data=data, columns=["slope", "runoff"])
print(df.head(10))