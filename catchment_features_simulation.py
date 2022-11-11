import os
import swmmio
import tempfile
import shutil
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from swmmio.utils.dataframes import dataframe_from_inp
from swmmio.utils.text import get_inp_sections_details
from swmmio.utils.modify_model import replace_inp_section
from swmmio.version_control.utils import write_inp_section
from pyswmm import Simulation, Nodes, Links, Subcatchments, Output


class FeaturesSimulation:

    def __init__(self, subcatchemnt_id, raw_file):
        self.raw_file = raw_file
        self.subcatchemnt_id = subcatchemnt_id
        self.file = FeaturesSimulation.copy_file(self, copy=self.raw_file)

    def copy_file(self, copy=None, suffix="copy"):
        if copy is None:
            copy = self.raw_file
        model = swmmio.Model(copy)
        new_path = os.path.join(model.inp.name + "_" + suffix + ".inp")
        model.inp.save(new_path)
        return new_path

    def get_section(self, section="subcatchments"):
        return getattr(swmmio.Model(self.file).inp, section)

    # def get_section_headers(self, file=None):
    #     if file is None:
    #         file = self.file
    #     return swmmio.Model(file).inp.headers

    def simulate_percent_imprevious(self, start=0, stop=100, step=10):
        catchment_data = {"runoff": [], "peak_runoff_rate": [], "infiltration": [], "evaporation": []}
        model = swmmio.Model(self.file)
        percent_impervious = []

        for percent in range(start, stop, step):
            subcatchments = swmmio.utils.dataframes.dataframe_from_inp(model.inp.path, '[SUBCATCHMENTS]')
            percent_impervious.append(percent)
            subcatchments.loc[self.subcatchemnt_id, "PercImperv"] = percent
            swmmio.utils.modify_model.replace_inp_section(model.inp.path, '[SUBCATCHMENTS]', subcatchments)

            with Simulation(self.file) as sim:
                subcatchment = Subcatchments(sim)[self.subcatchemnt_id]
                for _ in sim:
                    pass
                subcatchemnt_stats = subcatchment.statistics
                for key in catchment_data:
                    catchment_data[key].append(subcatchemnt_stats[key])
        catchment_data["PercImperv"] = percent_impervious
        return pd.DataFrame(data=catchment_data)



obj = FeaturesSimulation(subcatchemnt_id="S1", raw_file='example.inp')
df = obj.simulate_percent_imprevious(start=10, stop=100, step=10)
df.to_excel('test.xlsx')