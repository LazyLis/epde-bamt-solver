import pandas as pd
import numpy as np
import torch

from func import load_data
from epde_general import epde_equations
from bamt_general import bs_experiment
from solver_general import solver_equations
from func import confidence_region as conf_plt

if __name__ == '__main__':

    tasks = {
        'wave_equation': load_data.wave_equation,
        'burgers_equation': load_data.burgers_equation,
        'KdV_equation': load_data.KdV_equation
    }

    title = list(tasks.keys())[0]  # name of the problem/equation

    u, grid_u, cfg, params, b_conds = tasks[title]()

    for variance in cfg.params["glob_epde"]["variance_arr"]:

        df_main, epde_search_obj = epde_equations(u, grid_u, cfg, variance, title)

        equations = bs_experiment(df_main, cfg, title)

        u_main, grid_main = solver_equations(cfg, params, b_conds, equations, epde_search_obj, title)

        conf_plt.confidence_region_print(u, cfg, params, u_main, grid_main, variance)
