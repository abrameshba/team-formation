#!/usr/bin/bash


year=2020

# remove existing files 
rm -v ./"dblp-"$year/*.txt
rm -v ./"dblp-"$year/*.xml


# extracting the .xml.gz file
gunzip -k ./"dblp-"$year/"dblp-"$year"-04-01.xml.gz"

# rearrange with newline for each tag closing
sed "s/></>\n</g" ./dblp-$year/dblp-$year-04-01.xml  > ./"dblp-"$year/t1.txt

# remove non-relevant tags 
grep -v "<note\|<cite\|<url\|<crossref\|<pages\|<volume\|<number\|<ee\|<cdrom\|<month\|<series\|<editor\|<publisher\|<isbn" ./"dblp-"$year/t1.txt > ./"dblp-"$year/t2.txt
rm -v ./"dblp-"$year/t1.txt
# extract all articles with () information
sed -n '/<article/,/<\/article>/p' ./"dblp-"$year/t2.txt | tr -d "\n" | sed 's/<article/\n<article/g' | sed 's/<\/article>/<\/article>\n/g' > ./"dblp-"$year/at3.txt

# remove attributes and values (mdate,key,pubtype of article and orcid of author)
sed 's/\smdate=\"[0-9-]*\"//g' ./"dblp-"$year/at3.txt	| sed 's/\skey=\"[a-z\/A-Z0-9-]*\"//g' | sed 's/\spubltype=\"[a-z\/A-A ]*\"//g' | sed 's/\sorcid=\"[0-9X\-]*\"//g' > ./"dblp-"$year/at4.txt
rm -v ./"dblp-"$year/at3.txt
# remove invalid entries  and tags (<article>, </article>)
grep -v 'publtype=\"withdrawn\"' ./"dblp-"$year/at4.txt | sed 's/<\/author>[[:space:]]*<author>/:/g' | sed '/^[[:space:]]*$/d' > ./"dblp-"$year/articles.txt
rm -v ./"dblp-"$year/at4.txt

# extract all conferences with () information
sed -n '/<inproceedings/,/<\/inproceedings>/p' ./"dblp-"$year/t2.txt | tr -d "\n" | sed 's/<inproceedings/\n<inproceedings/g' | sed 's/<\/inproceedings>/<\/inproceedings>\n/g' > ./"dblp-"$year/it3.txt
rm -v ./"dblp-"$year/t2.txt
# remove attributes and values (mdate,key,pubtype of article and orcid of author)
sed 's/\smdate=\"[0-9-]*\"//g' ./"dblp-"$year/it3.txt	| sed 's/\skey=\"[a-z\/A-Z0-9-]*\"//g' | sed 's/\spubltype=\"[a-z\/A-A ]*\"//g' | sed 's/\sorcid=\"[0-9X\-]*\"//g' > ./"dblp-"$year/it4.txt
rm -v ./"dblp-"$year/it3.txt
# remove invalid entries  and tags (<article>, </article>)
grep -v 'publtype=\"withdrawn\"' ./"dblp-"$year/it4.txt | sed 's/<\/author>[[:space:]]*<author>/:/g' | sed '/^[[:space:]]*$/d' > ./"dblp-"$year/inproceedings.txt
rm -v ./"dblp-"$year/it4.txt


