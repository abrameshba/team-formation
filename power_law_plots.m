#!/usr/bin/gnuplot -persist
year ="2015"
#pods www kdd sdm pkdd icdm icml ecml colt uai soda focs stoc stacs dm ai th dblp
do for [network in "dblp"] {
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
#set title "power law property by degree of experts of ".network." network"  tc "royalblue"
stats '../dblp-'.year.'/'.network.'-nodes.txt' u 1:2 nooutput
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Degree of experts"
set ylabel "Number of experts"
set logscale y
set logscale x
#stats '../dblp-'.year.'/'.network.'-skills-per-expert.txt' using 1 name "s" nooutput
#set x2range [s_min/2:s_max*2]
#set x2label "Skills per expert"
#set logscale x2
set output './eps/'.network.'-'.year.'-pl.eps'
f(x) = a * ( x ** b)
a=1000
b=-.10
#set fit quiet
fit f(x) '../dblp-'.year.'/'.network.'-nodes.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-hc.txt' using 1:2 with point pointtype 12 pointsize 2 lc rgb "#00FF00" title "high degree experts" axis x1y1,\
        '../dblp-'.year.'/'.network.'-lc.txt' using 1:2 with point pointtype 6 pointsize 2 lc rgb "#FF0000" title "low degree experts" axis x1y1
#        f(x) title "Degree power law"  lt 2 lw 1
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
#set title "Skills per Expert"
stats '../dblp-'.year.'/'.network.'-skills-per-expert.txt' u 1:2 nooutput
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Skills per expert"
set ylabel "Number of experts"
set logscale xy
set output './eps/'.network.'-'.year.'-skills-per-expert-pl.eps'
a=1000
b=-0.10
#set fit quiet
fit f(x) '../dblp-'.year.'/'.network.'-skills-per-expert.txt' via a, b
plot   '../dblp-'.year.'/'.network.'-skills-per-expert.txt' using 1:2 with point pointtype 3  pointsize 2 lc rgb "#0000FF" title "Number of experts"
#        f(x) title "skills per expert"  lt 2 lw 1
reset
set terminal postscript eps enhanced color font 'Arial-Bold'
#set title "Experts per skill"
stats '../dblp-'.year.'/'.network.'-experts-per-skill.txt' using 1:2 nooutput
#print(network)
avg=STATS_sumxy/STATS_sum_y
set xrange [STATS_min_x/2:STATS_max_x*2]
set yrange [STATS_min_y/2:STATS_max_y*2]
set xlabel "Experts per skill"
set ylabel "Number of skills"
set logscale xy
set arrow from avg,STATS_min_y to avg,STATS_max_y heads dt "."
set arrow from avg,STATS_max_y/2 to avg*2,STATS_max_y/2
set arrow from avg,STATS_min_y*2 to avg/2,STATS_min_y*2
set label "popular skills" at avg*2,STATS_max_y/2
set label "rare skills" at avg/6,STATS_min_y*2
set label sprintf("avg. number of experts per skill = %3.2f",avg) at avg/5,STATS_min_y-0.3
set output './eps/'.network.'-'.year.'-experts-per-skill-pl.eps'
a=1000
b=-0.10
#set fit quiet
#set boxwidth 0.9 relative
set style data histograms
set style histogram cluster
set style fill solid 0.5 border lt -1
fit f(x) '../dblp-'.year.'/'.network.'-experts-per-skill.txt' via a, b
plot    '../dblp-'.year.'/'.network.'-experts-per-skill.txt' using (($1>0)? $1 : 1/0):2  with point pointtype 3 pointsize 2 lc rgb "#0000FF" title "Number of skills"
#        f(x) title "eperts per skill"  lt 2 lw 1
}