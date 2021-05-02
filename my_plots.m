#!/usr/bin/gnuplot -persist
do for [network in "icdt pods edbt vldb icde sigmod db"] {
    reset
    #set title "Degree distribution" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task size"
    set terminal postscript eps enhanced color
    i = 14
    if (i == 8) {
        set ylabel "Shannon task diversity"
        set output network."-shannon-task-diversity.eps"
    }else{
        if (i == 12) {
            set ylabel "Simpson task diversity"
            set output network."-simpson-task-diversity.eps"
            set logscale y
        }else{
            set ylabel "Gini-Simpson task diversity"
            set output network."-gini-simpson-task-diversity.eps"
        }
    }
    plot    '../dblp-2015/'.network.'-17-tasks-0-tfs-results.txt' using 1:i with line linetype 2 lc rgb "#EE88EE" notitle,\
            '../dblp-2015/'.network.'-17-tasks-0-tfs-results.txt' using 1:i with points pointtype 1 lc rgb "#EE88EE" title "tfs",\
            '../dblp-2015/'.network.'-17-tasks-0-rfs-results.txt' using 1:i with line linetype 2 lc rgb "#EE2233" notitle,\
            '../dblp-2015/'.network.'-17-tasks-0-rfs-results.txt' using 1:i with points pointtype 2 lc rgb "#EE2233" title "rarestfirst",\
            '../dblp-2015/'.network.'-17-tasks-0-bsd-results.txt' using 1:i with line linetype 2 lc rgb "#222222" notitle,\
            '../dblp-2015/'.network.'-17-tasks-0-bsd-results.txt' using 1:i with points pointtype 3 lc rgb "#222222" title  "bsd"
    #         '../dblp-2015/'.network.'-17-tasks-0-mds-results.txt' using 1:i with line linetype 2 lc rgb "#555555" notitle,\
    #         '../dblp-2015/'.network.'-17-tasks-0-mds-results.txt' using 1:i with points pointtype 4 lc rgb "#555555" title  "mds"
    reset
    set key autotitle columnheader
    set xlabel "Task size"
    set terminal postscript eps enhanced color
    if (i == 8) {
        set ylabel "Shannon team diversity"
        set output network."-shannon-team-diversity.eps"
    }else{
        if (i == 12) {
            set ylabel "Simpson team diversity"
            set output network."-simpson-team-diversity.eps"
            set logscale y
        }else{
            set ylabel "Gini-Simpson team diversity"
            set output network."-gini-simpson-team-diversity.eps"
        }
    }
    j = i+1
    plot    '../dblp-2015/'.network.'-17-tasks-0-tfs-results.txt' using 1:j with line linetype 2 lc rgb "#EE88EE" notitle,\
            '../dblp-2015/'.network.'-17-tasks-0-tfs-results.txt' using 1:j with points pointtype 1 lc rgb "#EE88EE" title "tfs",\
            '../dblp-2015/'.network.'-17-tasks-0-rfs-results.txt' using 1:j with line linetype 2 lc rgb "#EE2233" notitle,\
            '../dblp-2015/'.network.'-17-tasks-0-rfs-results.txt' using 1:j with points pointtype 2 lc rgb "#EE2233" title "rarestfirst",\
            '../dblp-2015/'.network.'-17-tasks-0-bsd-results.txt' using 1:j with line linetype 2 lc rgb "#222222" notitle,\
            '../dblp-2015/'.network.'-17-tasks-0-bsd-results.txt' using 1:j with points pointtype 3 lc rgb "#222222" title  "bsd"
    #         '../dblp-2015/'.network.'-17-tasks-0-mds-results.txt' using 1:j with line linetype 2 lc rgb "#555555" notitle,\
    #         '../dblp-2015/'.network.'-17-tasks-0-mds-results.txt' using 1:j with points pointtype 4 lc rgb "#555555" title  "mds"
}