#!/usr/bin/gnuplot -persist
year ="2015"
#  sigmod icde icdt edbt pods www kdd sdm pkdd icdm icml ecml colt uai soda focs stoc stacs db
do for [network in  "vldb"] {
    reset
    #set title "Processing time (sec)" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task Size |T|"
    stats '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt'  using 2 name "tfr" nooutput
    stats '../dblp-'.year.'/'.network.'-170-0-bld-results.txt'  using 2 name "bld" nooutput
    set xrange [3:21]
    set yrange [tfr_min/2:bld_max*100]
    set logscale y
    set key box Left left
    set terminal postscript eps enhanced color
    set ylabel "Processing time (sec)"
    set output './eps/'.network."-rand-170-processing-time.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:2 with linespoints title "MinDiamSol",\
            '../dblp-'.year.'/'.network.'-170-0-bld-results.txt' using 1:2 with linespoints title "MinLD",\
            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:2 with linespoints title "MinSD",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:2 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfs-results1.txt' using 1:2 with linespoints title "TPLClosest-1",\
            '../dblp-'.year.'/'.network.'-170-0-tfs-results2.txt' using 1:2 with linespoints title "TPLClosest-2",\
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:2 with linespoints title "TPLRandom"


    reset
    #set title "Team size" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task Size |T|"
#    set logscale y
    set xrange [3:21]
    set key box Left left
    set terminal postscript eps enhanced color
    set ylabel "Team size |X|"
    set output './eps/'.network."-rand-170-team-size.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:3 with linespoints title "MinDiamSol",\
            '../dblp-'.year.'/'.network.'-170-0-bld-results.txt' using 1:3 with linespoints title "MinLD",\
            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:3 with linespoints title "MinSD",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:3 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfs-results1.txt' using 1:3 with linespoints title "TPLClosest-1",\
            '../dblp-'.year.'/'.network.'-170-0-tfs-results2.txt' using 1:3 with linespoints title "TPLClosest-2",\
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:3 with linespoints title "TPLRandom"
    reset
    #set title "Diameter" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task Size |T|"
#    set logscale y
    set xrange [3:21]
    set key box Left left
    set terminal postscript eps enhanced color
    set ylabel "Diameter"
    set output './eps/'.network."-rand-170-diameter.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:5 with linespoints title "MinDiamSol",\
            '../dblp-'.year.'/'.network.'-170-0-bld-results.txt' using 1:5 with linespoints title "MinLD",\
            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:5 with linespoints title "MinSD",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:5 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfs-results1.txt' using 1:5 with linespoints title "TPLClosest-1",\
            '../dblp-'.year.'/'.network.'-170-0-tfs-results2.txt' using 1:5 with linespoints title "TPLClosest-2",\
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:5 with linespoints title "TPLRandom"
    reset
    #set title "Leader distance" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task Size |T|"
#    set logscale y
    set xrange [3:21]
    set key box Left left
    set terminal postscript eps enhanced color
    set ylabel "Leader distance"
    set output './eps/'.network."-rand-170-leader-distance.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:6 with linespoints title "MinDiamSol",\
            '../dblp-'.year.'/'.network.'-170-0-bld-results.txt' using 1:6 with linespoints title "MinLD",\
            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:6 with linespoints title "MinSD",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:6 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfs-results1.txt' using 1:6 with linespoints title "TPLClosest-1",\
            '../dblp-'.year.'/'.network.'-170-0-tfs-results2.txt' using 1:6 with linespoints title "TPLClosest-2",\
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:6 with linespoints title "TPLRandom"
    reset
    #set title "Leader sum distance" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task Size |T|"
#    set logscale y
    set xrange [3:21]
    set key box Left left
    set terminal postscript eps enhanced color
    set ylabel "Leader sum distance"
    set output './eps/'.network."-rand-170-leader-sum-distance.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:7 with linespoints title "MinDiamSol",\
            '../dblp-'.year.'/'.network.'-170-0-bld-results.txt' using 1:7 with linespoints title "MinLD",\
            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:7 with linespoints title "MinSD",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:7 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfs-results1.txt' using 1:7 with linespoints title "TPLClosest-1",\
            '../dblp-'.year.'/'.network.'-170-0-tfs-results2.txt' using 1:7 with linespoints title "TPLClosest-2",\
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:7 with linespoints title "TPLRandom"
    reset
    #set title "Sum distance" font ",14" textcolor rgbcolor "royalblue"
    set xlabel "Task Size |T|"
#     set logscale y
    set xrange [3:21]
    set key box Left left
    set terminal postscript eps enhanced color
    set ylabel "Sum distance"
    set output './eps/'.network."-rand-170-sum-distance.eps"
    plot    '../dblp-'.year.'/'.network.'-170-0-mds-results.txt' using 1:8 with linespoints title "MinDiamSol",\
            '../dblp-'.year.'/'.network.'-170-0-bld-results.txt' using 1:8 with linespoints title "MinLD",\
            '../dblp-'.year.'/'.network.'-170-0-bsd-results.txt' using 1:8 with linespoints title "MinSD",\
            '../dblp-'.year.'/'.network.'-170-0-rfs-results.txt' using 1:8 with linespoints title "Rarestfirst", \
            '../dblp-'.year.'/'.network.'-170-0-tfs-results1.txt' using 1:8 with linespoints title "TPLClosest-1",\
            '../dblp-'.year.'/'.network.'-170-0-tfs-results2.txt' using 1:8 with linespoints title "TPLClosest-2",\
            '../dblp-'.year.'/'.network.'-170-0-tfr-results.txt' using 1:8 with linespoints title "TPLRandom"
}