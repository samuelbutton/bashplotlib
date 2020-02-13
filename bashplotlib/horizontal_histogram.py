#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based histograms
"""

from __future__ import print_function
from __future__ import division

import os
import sys
import math
import optparse
from os.path import dirname
from .utils.helpers import *
from .utils.commandhelp import hist


def calc_bins(n, min_val, max_val, h=None, binwidth=None):
    """
    Calculate number of bins for the histogram
    """
    if not h:
        h = max(10, math.log(n + 1, 2))
    if binwidth == 0:
        binwidth = 0.1
    if binwidth is None:
        binwidth = (max_val - min_val) / h
    for b in drange(min_val, max_val, step=binwidth, include_stop=True):
        if b.is_integer():
            yield int(b)
        else:
            yield b


def read_numbers(numbers):
    """
    Read the input data in the most optimal way
    """
    if isiterable(numbers):
        for number in numbers:
            yield float(str(number).strip())
    else:
        with open(numbers) as fh:
            for number in fh:
                yield float(number.strip())


def run_demo():
    """
    Run a demonstration
    """
    module_dir = dirname(dirname(os.path.realpath(__file__)))
    demo_file = os.path.join(module_dir, 'examples/data/exp.txt')

    if not os.path.isfile(demo_file):
        sys.stderr.write("demo input file not found!\n")
        sys.stderr.write("run the downloaddata.sh script in the example first\n")
        sys.exit(1)

    # plotting a histogram
    print("plotting a basic histogram")
    print("plot_horiz_hist('%s')" % demo_file)
    print("hist -f %s" % demo_file)
    print("cat %s | hist" % demo_file)
    plot_horiz_hist(demo_file)
    print("*" * 80)

    # with colours
    print("histogram with colours")
    print("plot_horiz_hist('%s', colour='blue')" % demo_file)
    print("hist -f %s -c blue" % demo_file)
    plot_horiz_hist(demo_file, colour='blue')
    print("*" * 80)

    # changing the shape of the point
    print("changing the shape of the bars")
    print("plot_horiz_hist('%s', pch='.')" % demo_file)
    print("hist -f %s -p ." % demo_file)
    plot_horiz_hist(demo_file, pch='.')
    print("*" * 80)

    # changing the size of the plot
    print("changing the size of the plot")
    print("plot_horiz_hist('%s', width=35.0, bincount=40)" % demo_file)
    print("hist -f %s -s 35.0 -b 40" % demo_file)
    plot_horiz_hist(demo_file, width=35.0, bincount=40)


def plot_horiz_hist(f, width=20.0, bincount=None, binwidth=None, pch="o", colour="default", title="", xlab=None, showSummary=False, regular=False, xtitle=None, ytitle=None):
    """
    Make a histogram

    Arguments:
        width -- the width of the histogram in # of characters
        bincount -- number of bins in the histogram
        binwidth -- width of bins in the histogram
        pch -- shape of the bars in the plot
        colour -- colour of the bars in the terminal
        title -- title at the top of the plot
        xlab -- boolen value for whether or not to display x-axis labels
        showSummary -- boolean value for whether or not to display a summary
        regular -- boolean value for whether or not to start y-labels at 0
    """
    if pch is None:
        pch = "o"

    if isinstance(f, str):
        with open(f) as fh:
            f = fh.readlines()

    min_val, max_val = None, None
    n, mean, sd = 0.0, 0.0, 0.0

    for number in read_numbers(f):
        n += 1
        if min_val is None or number < min_val:
            min_val = number
        if max_val is None or number > max_val:
            max_val = number
        mean += number

    mean /= n

    for number in read_numbers(f):
        sd += (mean - number)**2

    sd /= (n - 1)
    sd **= 0.5

    bins = list(calc_bins(n, min_val, max_val, bincount, binwidth))
    hist = dict((i, 0) for i in range(len(bins)))

    for number in read_numbers(f):
        for i, b in enumerate(bins):
            if number <= b:
                hist[i] += 1
                break
        if number == max_val and max_val > bins[len(bins) - 1]:
            hist[len(hist) - 1] += 1

    min_y, max_y = min(hist.values()), max(hist.values())

    start = max(min_y, 1)
    stop = max_y + 1

    if regular:
        start = 1

    if width is None:
        width = stop - start
        if width > 20:
            width = 20

    ys = list(drange(start, stop, float(stop - start) / width))
    ys.reverse()

    nlen = max(len(str(min_y)), len(str(max_y))) + 1

    max_bin, min_bin = min(hist.keys()), max(hist.keys())
    binlen = max(len(str(min_bin)), len(str(max_bin)))

    if title:
        print(box_text([title], max(len(hist) * 2, len(title)), nlen))
    print()

    if xtitle: 
        print(" " + "x: "+ xtitle   )
        # return_string += "y: "+ ytitle  + "\n"


    start = min_val
    stop = max_val + 1
    num_buckets = 11
    xs = list(drange(start, stop, float(stop - start) / num_buckets))

    if xlab:
        index = 0
        for x in xs:
            binlab = str(int(x))
            binlab = " " * (binlen - len(binlab)) + binlab + "|"
            print(binlab, end=' ')

            bin_sum = 0
            for i in hist.keys():
                if i >= index and i <= x:
                    bin_sum += hist[i]
                    index = i + 1
            
            for y in ys:
                if bin_sum >= y:
                    printcolour(pch, True, colour)
            print('')
    
    print(" " * (nlen + 1) + "-" * len(ys))

    ys.reverse()
    print(get_y_label(ys, binlen))


    if ytitle: 
        full_title = "y: "+ ytitle
        print(" " * ((nlen + 1) + len(xs) - len(full_title)) + full_title)
        # return_string += " " * (xs - len(full_title)) + full_title  + "\n"

    center = max(map(len, map(str, [n, min_val, mean, max_val])))
    center += 15

    if showSummary:
        print()
        title = ["Summary"]
        print(box_text(title, max(len(hist) * 2, len(title)), nlen))
        stats = ["observations: %d" % n, "min value: %f" % min_val,
        "mean : %f" % mean, "std dev : %f" % sd, "max value: %f" % max_val]
        print(box_text(stats, max(len(hist) * 2, len(title)), nlen))

def get_y_label(ys, binlen):
    y_master_label = ""
    ys_copy = ys[:]

    used_labels = set()
    for (i, y) in enumerate(ys_copy):
        y = int(y)
        if y in used_labels:
            ys_copy[i] = 0
        else: 
            ys_copy[i] = int(y)
            used_labels.add(y)

    zeros = len(ys)*[0]
    continue_build = True

    

    while continue_build:
        y_master_label += " " * (binlen + 2)
        power_of_ten = 10

        for (i, y) in enumerate(ys_copy):
            if y < 1:
                if zeros[i] > 0:
                    y_master_label += "0"   
                else:
                    y_master_label += " "
            else:
                while y >= power_of_ten:
                    power_of_ten *= 10
                    zeros[i] += 1
                add_val = y // (power_of_ten/10)
                y_master_label += str(int(add_val))
                # print(ys_copy)
                ys_copy[i] -= add_val * (power_of_ten/10)
                zeros[i] -= 1
        
        continue_build = False
        for y in ys_copy:
            if y > 0:
                continue_build = True
                y_master_label += "\n"
                break
    return y_master_label

def main():

    parser = optparse.OptionParser(usage=hist['usage'])

    parser.add_option(
        '-f', '--file', help='a file containing a column of numbers', default=None, dest='f')
    parser.add_option('-t', '--title', help='title for the chart', default="", dest='t')
    parser.add_option(
        '-b', '--bins', help='number of bins in the histogram', type='int', default=None, dest='b')
    parser.add_option('-w', '--binwidth', help='width of bins in the histogram',
                      type='float', default=None, dest='binwidth')
    parser.add_option('-s', '--width', help='width of the histogram (in lines)',
                      type='int', default=None, dest='h')
    parser.add_option('-p', '--pch', help='shape of each bar', default='o', dest='p')
    parser.add_option('-x', '--xlab', help='label bins on x-axis',
                      default=None, action="store_true", dest='x')
    parser.add_option('-c', '--colour', help='colour of the plot (%s)' %
                      colour_help, default='default', dest='colour')
    parser.add_option('-d', '--demo', help='run demos', action='store_true', dest='demo')
    parser.add_option('-n', '--nosummary', help='hide summary',
                      action='store_false', dest='showSummary', default=True)
    parser.add_option('-r', '--regular',
                      help='use regular y-scale (0 - maximum y value), instead of truncated y-scale (minimum y-value - maximum y-value)',
                      default=False, action="store_true", dest='regular')

    opts, args = parser.parse_args()

    if opts.f is None:
        if len(args) > 0:
            opts.f = args[0]
        elif opts.demo is None or opts.demo is False:
            opts.f = sys.stdin.readlines()

    if opts.demo:
        run_demo()
    elif opts.f:
        plot_hist(opts.f, opts.h, opts.b, opts.binwidth, opts.p, opts.colour,
                  opts.t, opts.x, opts.showSummary, opts.regular)
    else:
        print("nothing to plot!")


if __name__ == "__main__":
    main()
