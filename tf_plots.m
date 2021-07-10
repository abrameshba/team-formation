#!/usr/bin/gnuplot -persist
year ="2015"
#  sigmod icde icdt edbt pods www kdd sdm pkdd icdm icml ecml colt uai soda focs stoc stacs db
do for [network in  "vldb"] {
    reset
    #set title "Processing time" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
#    set logscale y
    set key left
    set terminal postscript eps enhanced color
    set ylabel "processing-time"
    set output './eps/'.network."-rand-170-processing-time.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-tfs-results.txt' using 1:2 with linespoints title "TPLClosest",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:2 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:2 with linespoints title "TPLRandom"
#            '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:2 with linespoints title "2015-mds",\
#            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
    reset
    #set title "Team size" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
#    set logscale y
    set key left
    set terminal postscript eps enhanced color
    set ylabel "team size"
    set output './eps/'.network."-rand-170-team-size.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-tfs-results.txt' using 1:3 with linespoints title "TPLClosest",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:3 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:3 with linespoints title "TPLRandom"
#            '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:2 with linespoints title "2015-mds",\
#            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
    reset
    #set title "diameter" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
#    set logscale y
    set key left
    set terminal postscript eps enhanced color
    set ylabel "Diameter"
    set output './eps/'.network."-rand-170-diameter.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-tfs-results.txt' using 1:5 with linespoints title "TPLClosest",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:5 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:5 with linespoints title "TPLRandom"
#            '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:2 with linespoints title "2015-mds",\
#            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
    reset
    #set title "leader-sum-distance" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
#    set logscale y
    set key left
    set terminal postscript eps enhanced color
    set ylabel "leader-sum-distance"
    set output './eps/'.network."-rand-170-leader-sum-distance.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-tfs-results.txt' using 1:7 with linespoints title "TPLClosest",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:7 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:7 with linespoints title "TPLRandom"
#            '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:2 with linespoints title "2015-mds",\
#            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
    reset
    #set title "sum distance" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "frequent skills"
#     set logscale y
    set key left
    set terminal postscript eps enhanced color
    set ylabel "sum distance"
    set output './eps/'.network."-rand-170-sum-distance.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-tfs-results.txt' using 1:8 with linespoints title "TPLClosest",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:8 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:8 with linespoints title "TPLRandom"
#            '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:2 with linespoints title "2015-mds",\
#            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:2 with linespoints title "2015-bsd"
}