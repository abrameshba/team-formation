#!/usr/bin/gnuplot -persist
year ="2015"
do for [network in "icdt pods edbt vldb icde sigmod db"] {
reset
set xlabel "Degree"
set ylabel "Frequency"
set logscale xy
set terminal postscript eps enhanced color
set output network.year.'-pl.eps'
plot    '../dblp-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 2 lc rgb "#00FF00" title "high collaborating experts",\
        '../dblp-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 3 lc rgb "#FF0000" title "low collaborating experts"
reset
set title "Expert skills histogram"
set xlabel "No of skills of an expert"
set ylabel "No of experts"
set logscale xy
set terminal postscript eps enhanced color
set output network.year.'-expt-skl-pl.eps'
plot    '../dblp-'.year.'/'.network.'-expt-skl-freq.txt' using 1:2 with point pointtype 2 lc rgb "#FF0000" title "number of experts"
reset
set title "experts for a skillhistogram"
set xlabel "No of experts for a skill"
set ylabel "No of skills"
set label "common skills" at 1000,2
set label "rare skills" at 5,40
set logscale xy
set terminal postscript eps enhanced color
set output network.year.'-skl-expt-pl.eps'
plot    '../dblp-'.year.'/'.network.'-skl-expt-freq.txt' using 1:2 with point pointtype 2 lc rgb "#FF0000" title "number of experts"
}