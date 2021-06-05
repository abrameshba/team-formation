#!/usr/bin/gnuplot -persist
year ="2015"
do for [network in "vldb sigmod icde icdt edbt pods www kdd sdm pkdd icdm icml ecml colt uai soda focs stoc stacs db dm ai th dblp"] {
#do for [network in "dblp"] {
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "Degree of experts"
stats '../dblp-'.year.'/'.network.'-nodes.txt' u 1:2 nooutput
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Degree of experts"
set ylabel "Number of experts"
set logscale xy
set output network.'-'.year.'-pl.eps'
f(x) = a * ( x ** b)
a=1000
b=-.10
set fit quiet
fit f(x) '../dblp-'.year.'/'.network.'-nodes.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 6 pointsize 2 lc rgb "#00FF00" title "high collaborating experts",\
        '../dblp-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 3 pointsize 2 lc rgb "#FF0000" title "low collaborating experts"
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
set output network.'-'.year.'-skills-per-expert-pl.eps'
a=1000
b=-0.10
set fit quiet
fit f(x) '../dblp-'.year.'/'.network.'-skills-per-expert.txt' via a, b
plot   '../dblp-'.year.'/'.network.'-skills-per-expert.txt' using 1:2 with point pointtype 3  pointsize 2 lc rgb "#0000FF" title "Number of experts"
#        f(x)  title "power law" lt 2 lw 1
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
set title "Experts per skill"
stats '../dblp-'.year.'/'.network.'-experts-per-skill.txt' using 1:2 nooutput
#print(network)
avg=STATS_sumxy/STATS_sum_y
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Experts per skill"
set ylabel "Number of skills"
set logscale xy
set arrow from avg,STATS_min_y to avg,STATS_max_y heads dt "."
set arrow from avg,STATS_max_y-10 to avg*2,STATS_max_y-10
set arrow from avg,STATS_min_y+2 to STATS_mean_y-2,STATS_min_y+2
set label "frequent skills" at avg*2,STATS_max_y-5
set label "rare skills" at STATS_mean_y/5,STATS_min_y+3
set label "avg experts per skill" at avg/5,STATS_min_y-0.3
set output network.'-'.year.'-experts-per-skill-pl.eps'
a=1000
b=-0.10
set fit quiet
set boxwidth 0.9 relative
set style data histograms
set style histogram cluster
set style fill solid 0.5 border lt -1
fit f(x) '../dblp-'.year.'/'.network.'-experts-per-skill.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-experts-per-skill.txt' using 1:2 with point pointtype 3 pointsize 2 lc rgb "#0000FF" title "Number of skills"
#plot   '../dblp-'.year.'/'.network.'-experts-per-skill.txt' using 1:2 smooth freq with boxes title "Number of skills"
#        f(x)  title "power law" lt 2 lw 1
#print "".network."".a."".b.""
#print("a=%1.2f",a)
#print("b=%1.2f",b)
}