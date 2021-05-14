#!/usr/bin/gnuplot -persist
year ="2015"
do for [network in "pods edbt vldb icde sigmod db"] {
reset
set title "Degree of experts histogram"
stats '../dblp-'.year.'/'.network.'-nodes.txt' u 1:2
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Degree"
set ylabel "Frequency"
set logscale xy
set terminal postscript eps enhanced color
set output network.'-'.year.'-pl.eps'
f(x) = a * ( x ** b)
stats '../dblp-'.year.'/'.network.'-nodes.txt' u 1:2
a=1000
b=-.10
fit f(x) '../dblp-'.year.'/'.network.'-nodes.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 4 pointsize 2 lc rgb "#00FF00" title "high collaborating experts",\
        '../dblp-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 3 pointsize 2 lc rgb "#FF0000" title "low collaborating experts"
#        f(x)  title "power law" lt 2 lw 1
reset
set encoding utf8
set title "Skills of an Expert histogram"
stats '../dblp-'.year.'/'.network.'-expt-freq.txt' u 1:2
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "No of skills of an expert"
set ylabel "No of experts"
set logscale xy
set terminal postscript eps enhanced color  font "sans,14"
set output network.'-'.year.'-expt-skl-pl.eps'
a=1000
b=-0.10
fit f(x) '../dblp-'.year.'/'.network.'-expt-freq.txt' via a, b
plot   '../dblp-'.year.'/'.network.'-expt-freq.txt' using 1:2 with point pointtype "\U+1234"  pointsize 3 lc rgb "#FF0000" title "Number of experts"
#        f(x)  title "power law" lt 2 lw 1
reset
set title "Experts for a skill histogram"
stats '../dblp-'.year.'/'.network.'-skl-freq.txt' u 1:2
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Number of experts for a skill : rare skills -> abundant skills"
set ylabel "Number of skills"
set logscale xy
set terminal postscript eps enhanced color  font "sans,14"
set output network.'-'.year.'-skl-expt-pl.eps'
a=1000
b=-0.10
set boxwidth 0.9 relative
set style data histograms
set style histogram cluster
set style fill solid 0.5 border lt -1
fit f(x) '../dblp-'.year.'/'.network.'-skl-freq.txt' via a, b
#plot   [STATS_min_x:STATS_max_x][STATS_min_y:STATS_max_y] '../dblp-'.year.'/'.network.'-skl-freq.txt' using 1:2 with point pointtype 2 pointsize 3 lc rgb "#FF0000" title "Number of skills"
plot   '../dblp-'.year.'/'.network.'-skl-freq.txt' using 1:2 smooth freq with boxes title "Number of skills"
#        f(x)  title "power law" lt 2 lw 1
}