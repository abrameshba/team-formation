#!/usr/bin/gnuplot -persist
reset
set title "Degree distribution" font ",14" textcolor rgbcolor "royalblue"
set ylabel "Number of scientists"
set xlabel "Degree of scientists"
set logscale xy
set terminal postscript eps enhanced color 
#set terminal pdfcairo 
set output "17MCPC02-1.eps"
set style histogram rowstacked gap 0
set style fill solid 0.5 border lt -1
plot 'jdblp.txt' using 1:2 smooth freq with boxes notitle

reset
#set title "Power law" font ",14" textcolor rgbcolor "royalblue"
set ylabel "Number of scientists"
set xlabel "Degree of scientists"
set logscale xy
set terminal postscript eps enhanced color 
#set terminal pdfcairo 
set output "17MCPC02-2.eps"
f(x) = a * ( x ** b)
a=225350
b=-.83
fit f(x) 'jdblp.txt' via a, b
plot 'jdblp.txt' using 1:2 with points pointtype 3 pointsize 1  lc rgb "#EE82EE" title "scientists", f(x)  title "power law" lt 2 lw 1
