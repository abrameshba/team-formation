#!/usr/bin/gnuplot -persist
year ="2015"
#do for [network in  "icdt stoc icml stoc icml sigmod stacs uai soda www edbt kdd sdm icde"] {
    reset
    #set title "Processing time" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "communities in increasing order"
#    set yrange [5:10]
    set logscale y
    set terminal postscript eps enhanced color
    set ylabel "all-processing-time"
    set output "all-10-processing-time.eps"
    plot    '../dblp-'.year.'/'.'all_tfs.txt' using 2:3 with linespoints  ps 2 title"2015-tfs",\
            '../dblp-'.year.'/'.'all_tfr.txt' using 2:3 with linespoints  ps 2 title "2015-tfr",\
            '../dblp-'.year.'/'.'all_rfs.txt' using 2:3 with linespoints  ps 2 title "2015-rfs"
#            '../dblp-'.year.'/'.network.'-10-0-mds-results.txt' using 1:2 with linespoints title "2015-mds",\
#            '../dblp-'.year.'/'.network.'-10-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
#}