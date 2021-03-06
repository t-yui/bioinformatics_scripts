#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
"""


import pandas as pd
from matplotlib import pyplot as plt
import argparse


def argParse():
    parser = argparse.ArgumentParser(
                add_help=True
                )
    parser.add_argument(
        '-e',
        '--eigenvec',
        dest='eigenvec',
        type=str,
        required=True
        )
    parser.add_argument(
        '-p',
        '--population',
        dest='population',
        type=str,
        required=True
        )
    parser.add_argument(
        '-o',
        '--outdir',
        dest='outdir',
        type=str,
        required=True
        )
    args = parser.parse_args()
    return args


def plotPCA(component_1, component_2, groups, outpath="./"):
    """
    Plot PCA results of GWAS data, which are processed by plink.

    Parameters
    ----------
    component_1 : pandas.Series
        scores of principal component 1
    component_2 : pandas.Series
        scores of principal component 2
    groups : pandas.Series
        groups that each individual belongs to
    outpath : str
        path to which images are output
    """
    # preparation
    uniq_groups = pd.Series.unique(groups)
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # plot all group
    plt.figure(figsize = [7, 5])
    for i in range(len(uniq_groups)):
        group = uniq_groups[i]
        plt.scatter(
            component_1[groups == group],
            component_2[groups == group],
            label = group,
            c = colors[i]
        )
    plt.title("RESULT OF PCA", size = 14)
    plt.xlabel("COMPONENT 1")
    plt.ylabel("COMPONENT 2")
    plt.legend()
    plt.savefig('{0}pca.png'.format(outpath))

    # plot by each group
    for i in range(len(uniq_groups)):
        plt.figure(figsize = [7, 5])
        group = uniq_groups[i]
        plt.scatter(
            component_1[groups == group],
            component_2[groups == group],
            label = group,
            c = colors[i]
        )
        plt.title("RESULT OF PCA : " + group, size = 14)
        plt.xlabel("COMPONENT 1")
        plt.ylabel("COMPONENT 2")
        plt.legend()
        plt.savefig('{0}pca_{1}.png'.format(outpath, group))


if __name__ == '__main__':
    args = argParse()

    # get arguments
    eigenvec = args.eigenvec
    population = args.population
    outdir = args.outdir

    # PATH for data
    eigenvecs_path = eigenvec
    population_path = population

    # import data
    df_eigenvecs = pd.read_csv(
        eigenvecs_path,
        header=None,
        delim_whitespace = True
    )
    df_population = pd.read_csv(
        population_path,
        header=None,
        delim_whitespace = True
    )

    # preprocess data
    df_population = df_population.rename(columns={2 : 'race'})
    df_merged = pd.merge(df_eigenvecs, df_population, on=[0, 1])
    df_pca = df_merged[[2, 3, 'race']]

    # inputs of plot
    component_1 = df_pca[2]
    component_2 = df_pca[3]
    groups = df_pca['race']

    plotPCA(
        component_1=component_1,
        component_2=component_2,
        groups=groups,
        outpath=outdir
    )
