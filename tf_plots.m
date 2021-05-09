#!/usr/bin/gnuplot -persist
year ="2020"
do for [network in "pods edbt vldb icde sigmod db"] {
    reset
    #set title "Degree distribution" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task size"
    set logscale y
    set terminal postscript eps enhanced color
    set ylabel "Processing time"
    set output network.year."dist-20-processing-time.eps"
    plot    '../dblp-'.year.'/'.network.'-20-0-tfs-results.txt' using 1:2 with line linetype 2 lc rgb "#EE88EE" notitle,\
            '../dblp-'.year.'/'.network.'-20-0-tfs-results.txt' using 1:2 with points pointtype 1 lc rgb "#EE88EE" title "tfs",\
            '../dblp-'.year.'/'.network.'-20-0-rfs-results.txt' using 1:2 with line linetype 2 lc rgb "#EE2233" notitle,\
            '../dblp-'.year.'/'.network.'-20-0-rfs-results.txt' using 1:2 with points pointtype 2 lc rgb "#EE2233" title "rarestfirst"
    #        '../dblp-'.year.'/'.network.'-20-0-bsd-results.txt' using 1:i with line linetype 2 lc rgb "#222222" notitle
    #        '../dblp-'.year.'/'.network.'-20-0-bsd-results.txt' using 1:i with points pointtype 3 lc rgb "#222222" title  "bsd"
    #         '../dblp-'.year.'/'.network.'-20-0-mds-results.txt' using 1:i with line linetype 2 lc rgb "#555555" notitle,\
    #         '../dblp-'.year.'/'.network.'-20-0-mds-results.txt' using 1:i with points pointtype 4 lc rgb "#555555" title  "mds"
}