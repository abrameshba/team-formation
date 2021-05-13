#!/usr/bin/gnuplot -persist
year ="2015"
yeart = "2020"
do for [network in "pods edbt vldb icde sigmod db"] {
    reset
    #set title "Degree distribution" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Common skills"
    set logscale y
    set terminal postscript eps enhanced color
    set ylabel "Processing time"
    set output network."-dist-20-processing-time.eps"
    plot    '../dblp-'.year.'/'.network.'-20-0-tfs-results.txt' using 1:2 with line linetype 2 lc rgb "#EE88EE" notitle,\
            '../dblp-'.year.'/'.network.'-20-0-tfs-results.txt' using 1:2 with points pointtype 1 lc rgb "#EE88EE" title "2015-tfs",\
            '../dblp-'.year.'/'.network.'-20-0-rfs-results.txt' using 1:2 with line linetype 2 lc rgb "#EE2233" notitle,\
            '../dblp-'.year.'/'.network.'-20-0-rfs-results.txt' using 1:2 with points pointtype 2 lc rgb "#EE2233" title "2015-rarestfirst", \
            '../dblp-'.yeart.'/'.network.'-20-0-tfs-results.txt' using 1:2 with line linetype 2 lc rgb "#EE88EE" notitle,\
            '../dblp-'.yeart.'/'.network.'-20-0-tfs-results.txt' using 1:2 with points pointtype 3 lc rgb "#EE88EE" title "2020-tfs",\
            '../dblp-'.yeart.'/'.network.'-20-0-rfs-results.txt' using 1:2 with line linetype 2 lc rgb "#EE2233" notitle,\
            '../dblp-'.yeart.'/'.network.'-20-0-rfs-results.txt' using 1:2 with points pointtype 4 lc rgb "#EE2233" title "2020-rarestfirst"
}