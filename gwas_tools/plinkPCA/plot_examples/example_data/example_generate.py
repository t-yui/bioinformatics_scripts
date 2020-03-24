#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pandas as pd
import numpy as np


if __name__ == '__main__':
    n_fams = 100
    n_inds = 3
    n_groups = 3
    p = 0.3
    mu_0 = 0
    mu_1 = 1

    eigenvec_data = {
        "FamID" : [],
        "IndID" : [],
        "PC1" : [],
        "PC2" : []
    }

    population_data = {
        "FamID" : [],
        "IndID" : [],
        "Group" : []
    }

    for g in range(n_groups):
        grp = "GROUP{0}".format(g + 1)
        pi = np.random.binomial(1, p)
        for i in range(n_fams):
            for j in range(n_inds):
                if pi == 0:
                    pc_1 = np.random.normal(mu_0)
                    pc_2 = np.random.normal(mu_0 + 0.5 + (g + 1)**2)
                else:
                    pc_1 = np.random.normal(mu_1)
                    pc_2 = np.random.normal(mu_1 + 0.5 + (g + 1)**2)
                eigenvec_data["FamID"].append("FAM{0}{1}".format(g, i))
                eigenvec_data["IndID"].append(j)
                eigenvec_data["PC1"].append(pc_1)
                eigenvec_data["PC2"].append(pc_2)
                population_data["FamID"].append("FAM{0}{1}".format(g, i))
                population_data["IndID"].append(j)
                population_data["Group"].append(grp)

    df_eigenvec = pd.DataFrame(eigenvec_data)
    df_population = pd.DataFrame(population_data)

    df_eigenvec.to_csv("./example.eigenvec", sep=" ", index=False, header=False)
    df_population.to_csv("./example_population.txt", sep=" ", index=False, header=False)
