#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based scatterplots
"""

from __future__ import print_function
import csv
import sys
import optparse
from .utils.helpers import *
from .utils.commandhelp import scatter


def get_scale(series, is_y=False, steps=20):
    min_val = min(series)
    max_val = max(series)
    scaled_series = []
    for x in drange(min_val, max_val, (max_val - min_val) / steps,
                    include_stop=True):
        if x > 0 and scaled_series and max(scaled_series) < 0:
            scaled_series.append(0.0)
        scaled_series.append(x)

    if is_y:
        scaled_series.reverse()
    return scaled_series


def build_scatter(xs, ys, size, pch, colour, title, cs, xtitle, ytitle):
    x_scale = get_scale(xs, False, size)
    y_scale = get_scale(ys, True, size)

    plotted = set()
    return_string = ""

    if title:
        return_string += box_text([title], 2 * (len(x_scale) + 1)) + "\n"

    if ytitle: 
        return_string += "y: "+ ytitle  + "\n"
    return_string += "+" + "-" * (2 * (len(x_scale) + 1)) + "+"  + "\n"
    
    for (i, y) in enumerate(y_scale):
        return_string += "| "
        addHoriz = False
        if y == 0.0:
            addHoriz = True
        for (j, x) in enumerate(x_scale):
            addVert = x == 0.0
            if addHoriz and addVert:
                point = "o"
            elif addHoriz:
                point = "-"
            elif addVert:
                point = "|"
            else:
                point = " "
            for (k, (xp, yp)) in enumerate(zip(xs, ys)):
                if xp <= x and yp >= y and (xp, yp) not in plotted:
                    point = pch
                    plotted.add((xp, yp))
                    if cs:
                        colour = cs[k]
            # return_string += getPointInColour(point + " ", True, colour)
            return_string += point + " "
            
        if addHoriz:
            return_string += "-|"  + "\n"
        else:
            return_string += " |"  + "\n"
        


    return_string += "+" + "-" * (2 * (len(x_scale) + 1)) + "+"  + "\n"
    if xtitle: 
        return_string += " " * (2 * (len(x_scale) + 2) - len("x: "+ xtitle)) + "x: "+ xtitle  + "\n"
    return return_string

def plot_scatter(f, xs, ys, size, pch, colour, title, xtitle=None, ytitle=None):
    """
    Form a complex number.

    Arguments:
        f -- comma delimited file w/ x,y coordinates
        xs -- if f not specified this is a file w/ x coordinates
        ys -- if f not specified this is a filew / y coordinates
        size -- size of the plot
        pch -- shape of the points (any character)
        colour -- colour of the points
        title -- title of the plot
        xtitle -- x axis title of the plot
        ytitle -- y axis title of the plot
    """
    cs = None
    if f:
        if isinstance(f, str):
            with open(f) as fh:
                data = [tuple(line.strip().split(',')) for line in fh]
        else:
            data = [tuple(line.strip().split(',')) for line in f]
        xs = [float(i[0]) for i in data]
        ys = [float(i[1]) for i in data]
        if len(data[0]) > 2:
            cs = [i[2].strip() for i in data]
    elif isinstance(xs, list) and isinstance(ys, list):
        pass
    else:
        with open(xs) as fh:
            xs = [float(str(row).strip()) for row in fh]
        with open(ys) as fh:
            ys = [float(str(row).strip()) for row in fh]

    graph_string = build_scatter(xs, ys, size, pch, colour, title, cs, xtitle, ytitle)
    print(graph_string)
    


def main():

    parser = optparse.OptionParser(usage=scatter['usage'])

    parser.add_option('-f', '--file', help='a csv w/ x and y coordinates', default=None, dest='f')
    parser.add_option('-t', '--title', help='title for the chart', default="", dest='t')
    parser.add_option('-x', help='x coordinates', default=None, dest='x')
    parser.add_option('-y', help='y coordinates', default=None, dest='y')
    parser.add_option('-s', '--size', help='y coordinates', default=20, dest='size', type='int')
    parser.add_option('-p', '--pch', help='shape of point', default="x", dest='pch')
    parser.add_option('h', '--xtitle', help='title for x axis', default=None, dest='h')
    parser.add_option('v', '--ytitle', help='title for y axis', default=None, dest='v')
    parser.add_option('-c', '--colour', help='colour of the plot (%s)' %
                      colour_help, default='default', dest='colour')

    opts, args = parser.parse_args()

    if opts.f is None and (opts.x is None or opts.y is None):
        opts.f = sys.stdin.readlines()

    if opts.f or (opts.x and opts.y):
        plot_scatter(opts.f, opts.x, opts.y, opts.size, opts.pch, opts.colour, opts.t, opts.h, opts.v)
    else:
        print("nothing to plot!")


if __name__ == "__main__":
    main()
