# scratch.py
from bashplotlib.horizontal_histogram import plot_horiz_hist

import random

nums = []
for i in range(1,100):
    nums.append(random.randint(1,100))

height = 200
bincount = 10
binwidth = 1
char = 'o'
color = 'default'
title = 'My Bar Chart'
displayXLabel = True
showSum = True
yStart = True


plot_horiz_hist(
    nums,
    height,
    bincount,
    binwidth,
    char,
    color,
    title,
    displayXLabel,
    showSum,
    yStart,
    xtitle="My x",
    ytitle="My y")