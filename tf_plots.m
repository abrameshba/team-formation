#!/usr/bin/gnuplot -persist
year ="2015"
yeart = "2020"
#do for [network in "colt ecml edbt focs icdt pkdd sigmod"] {
do for [network in "icdt sigmod"] {
    reset
    #set title "Processing time" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
#    set yrange [5:10]
    set logscale y
    set terminal postscript eps enhanced color
    set ylabel "processing-time"
    set output network."-rand-17-processing-time.eps"
    plot    '../dblp-'.year.'/'.network.'-10-0-tfs-results.txt' using 1:2 with linespoints title "2015-tfs",\
            '../dblp-'.year.'/'.network.'-10-0-rfs-results.txt' using 1:2 with linespoints title "2015-rarestfirst", \
            '../dblp-'.year.'/'.network.'-10-0-tfr-results.txt' using 1:2 with linespoints title "2015-tfr",\
            '../dblp-'.year.'/'.network.'-10-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
}