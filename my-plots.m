#!/usr/bin/gnuplot -persist
reset
#set title "Degree distribution" font ",14" textcolor rgbcolor "royalblue"
set ylabel "Shannon team gamma diversity"
set xlabel "Task size"
#set logscale xy
set terminal postscript eps enhanced color
#set terminal pdfcairo
set output "vldb-shannon-team-diversity.eps"
#set style histogram rowstacked gap 0
#set style fill solid 0.5 border lt -1
plot    '../dblp-2015/vldb-17-tasks-0-tfs-results.txt' using 1:9 with line linetype 2 lc rgb "#EE88EE" notitle,\
        '../dblp-2015/vldb-17-tasks-0-tfs-results.txt' using 1:9 with points pointtype 1 lc rgb "#EE88EE" title "tfs",\
        '../dblp-2015/vldb-17-tasks-0-rfs-results.txt' using 1:9 with line linetype 2 lc rgb "#EE2233" notitle,\
        '../dblp-2015/vldb-17-tasks-0-rfs-results.txt' using 1:9 with points pointtype 2 lc rgb "#EE2233" title "rarestfirst",\
        '../dblp-2015/vldb-17-tasks-0-bsd-results.txt' using 1:9 with line linetype 2 lc rgb "#222222" notitle,\
        '../dblp-2015/vldb-17-tasks-0-bsd-results.txt' using 1:9 with points pointtype 3 lc rgb "#222222" title  "bsd"

reset
#set title "Degree distribution" font ",14" textcolor rgbcolor "royalblue"
set ylabel "Shannon task gamma diversity"
set xlabel "Task size"
#set logscale xy
set terminal postscript eps enhanced color
#set terminal pdfcairo
set output "vldb-shannon-task-diversity.eps"
#set style histogram rowstacked gap 0
#set style fill solid 0.5 border lt -1
plot    '../dblp-2015/vldb-17-tasks-0-tfs-results.txt' using 1:8 with line linetype 2 lc rgb "#EE88EE" notitle,\
        '../dblp-2015/vldb-17-tasks-0-tfs-results.txt' using 1:8 with points pointtype 1 lc rgb "#EE88EE" title "tfs",\
        '../dblp-2015/vldb-17-tasks-0-rfs-results.txt' using 1:8 with line linetype 2 lc rgb "#EE2233" notitle,\
        '../dblp-2015/vldb-17-tasks-0-rfs-results.txt' using 1:8 with points pointtype 2 lc rgb "#EE2233" title "rarestfirst",\
        '../dblp-2015/vldb-17-tasks-0-bsd-results.txt' using 1:8 with line linetype 2 lc rgb "#222222" notitle,\
        '../dblp-2015/vldb-17-tasks-0-bsd-results.txt' using 1:8 with points pointtype 3 lc rgb "#222222" title  "bsd"


