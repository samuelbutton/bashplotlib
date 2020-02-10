# scratch.py
from bashplotlib.horizontal_histogram import plot_horiz_hist

nums = [0,10,15,5,5,5,5,5,5,5,5,10,10,10]
height = 20
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