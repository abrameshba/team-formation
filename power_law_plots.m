#!/usr/bin/gnuplot -persist
year ="2020"
do for [network in "pods edbt vldb icde sigmod db"] {
reset
set xlabel "Degree"
set ylabel "Frequency"
set logscale xy
set terminal postscript eps enhanced color
set output network.year.'-pl.eps'
f(x) = a * ( x ** b)
a=100
b=-.50
fit f(x) '../dblp-'.year.'/'.network.'-nodes.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 2 lc rgb "#00FF00" title "high collaborating experts",\
        '../dblp-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 3 lc rgb "#FF0000" title "low collaborating experts",\
        f(x)  title "power law" lt 2 lw 1
reset
#set title "Expert skills histogram"
set xlabel "No of skills of an expert"
set ylabel "No of experts"
set logscale xy
set terminal postscript eps enhanced color
set output network.year.'-expt-skl-pl.eps'
a=100
b=-0.50
fit f(x) '../dblp-'.year.'/'.network.'-expt-freq.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-expt-freq.txt' using 1:2 with point pointtype 2 lc rgb "#FF0000" title "number of experts",\
        f(x)  title "power law" lt 2 lw 1
reset
#set title "experts for a skill histogram"
set xlabel "No of experts for a skill"
set ylabel "No of skills"
set label "common skills" at 1000,2
set label "rare skills" at 5,40
set logscale xy
set terminal postscript eps enhanced color
set output network.year.'-skl-expt-pl.eps'
a=100
b=-0.50
fit f(x) '../dblp-'.year.'/'.network.'-skl-freq.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-skl-freq.txt' using 1:2 with point pointtype 2 lc rgb "#FF0000" title "number of experts",\
        f(x)  title "power law" lt 2 lw 1
}