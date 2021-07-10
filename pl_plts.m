#!/usr/bin/gnuplot -persist
year ="2015"
do for [network in "dblp"] {
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "power law property by degree of experts, skills per expert of ".network." network" tc "blue"
stats '../dblp-'.year.'/'.network.'-nodes.txt' u 1:2 nooutput
stats '../dblp-'.year.'/'.network.'-skills-per-expert.txt' using 1 name "s" nooutput
set xrange [STATS_min_x/2:STATS_max_x*2]
set x2range [s_min/2:s_max*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Degree of expert"
set x2label "Skills per expert"
set ylabel "Number of experts"
set logscale y
set logscale x
set logscale x2
set output './eps/'.network.'-'.year.'-pl.eps'
f(x) = a * ( x ** b)
a=1000
b=-.10
set fit quiet
fit f(x) '../dblp-'.year.'/'.network.'-nodes.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-skills-per-expert.txt' using 1:2 with point pointtype 1  pointsize 2 lc rgb "#0000FF" title "Number of experts"  axis x1y1,\
        '../dblp-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 10 pointsize 2 lc rgb "#00FF00" title "high degree experts" axis x2y1,\
        '../dblp-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 3 pointsize 2 lc rgb "#FF0000" title "low degree experts" axis x2y1
#        f(x)  title "power law" lt 2 lw 1
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "Skills of an Expert"
stats '../dblp-'.year.'/'.network.'-skills-per-expert.txt' u 1:2 nooutput
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "skills per expert"
set ylabel "Number of experts"
set logscale xy
set output './eps/'.network.'-'.year.'-skills-per-expert-pl.eps'
a=1000
b=-0.10
set fit quiet
fit f(x) '../dblp-'.year.'/'.network.'-skills-per-expert.txt' via a, b
plot   '../dblp-'.year.'/'.network.'-skills-per-expert.txt' using 1:2 with point pointtype 3  pointsize 2 lc rgb "#0000FF" title "Number of experts"
#        f(x)  title "power law" lt 2 lw 1
}
