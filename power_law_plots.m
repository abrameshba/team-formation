#!/usr/bin/gnuplot -persist
year ="2015"
#do for [network in "pods edbt vldb icde sigmod db"] {
do for [network in "bbsnm"] {
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "Degree of experts"
stats '../bbsnm-'.year.'/'.network.'-nodes.txt' u 1:2
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Degree of experts"
set ylabel "Number of experts"
set logscale xy
set output network.'-'.year.'-pl.eps'
f(x) = a * ( x ** b)
stats '../bbsnm-'.year.'/'.network.'-nodes.txt' u 1:2
a=1000
b=-.10
fit f(x) '../bbsnm-'.year.'/'.network.'-nodes.txt' via a, b
plot    '../bbsnm-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 6 pointsize 2 lc rgb "#00FF00" title "high collaborating experts",\
        '../bbsnm-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 3 pointsize 2 lc rgb "#FF0000" title "low collaborating experts"
#        f(x)  title "power law" lt 2 lw 1
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "Skills of an Expert"
stats '../bbsnm-'.year.'/'.network.'-expt-freq.txt' u 1:2
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Number of skills of an expert"
set ylabel "Number of experts"
set logscale xy
set output network.'-'.year.'-expt-skl-pl.eps'
a=1000
b=-0.10
fit f(x) '../bbsnm-'.year.'/'.network.'-expt-freq.txt' via a, b
plot   '../bbsnm-'.year.'/'.network.'-expt-freq.txt' using 1:2 with point pointtype 3  pointsize 2 lc rgb "#0000FF" title "Number of experts"
#        f(x)  title "power law" lt 2 lw 1
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "Experts for a skill"
stats '../bbsnm-'.year.'/'.network.'-skl-freq.txt' u 1:2
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Number of experts for a skill : rare skills -> abundant skills"
set ylabel "Number of skills"
set logscale xy
set arrow from STATS_mean_y,STATS_min_y to STATS_mean_y,STATS_max_y nohead dt "."
set output network.'-'.year.'-skl-expt-pl.eps'
a=1000
b=-0.10
set boxwidth 0.9 relative
set style data histograms
set style histogram cluster
set style fill solid 0.5 border lt -1
fit f(x) '../bbsnm-'.year.'/'.network.'-skl-freq.txt' via a, b
plot    '../bbsnm-'.year.'/'.network.'-skl-freq.txt' using 1:2 with point pointtype 3 pointsize 2 lc rgb "#0000FF" title "Number of skills"
#plot   '../bbsnm-'.year.'/'.network.'-skl-freq.txt' using 1:2 smooth freq with boxes title "Number of skills"
#        f(x)  title "power law" lt 2 lw 1
}