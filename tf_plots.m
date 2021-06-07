#!/usr/bin/gnuplot -persist
year ="2015"
yeart = "2020"
do for [network in "edbt sigmod colt ecml focs pkdd"] {
    reset
    #set title "Processing time" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
    set logscale y
    set terminal postscript eps enhanced color
    set ylabel "Processing time"
    set output network."-dist-15-processing-time.eps"
    plot    '../dblp-'.year.'/'.network.'-15-0-tfs-results.txt' using 1:2 with linespoints title "2015-tfs",\
            '../dblp-'.year.'/'.network.'-15-0-rfs-results.txt' using 1:2 with linespoints title "2015-rarestfirst", \
            '../dblp-'.year.'/'.network.'-15-0-tfr-results.txt' using 1:2 with linespoints title "2015-tfr"
}