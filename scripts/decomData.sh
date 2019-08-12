#! /bin/bash

# $1 >> nb days
# $2 >> input file
# $3 >> output file
# $4 >> nb_sec pour décomposer

# devise le temps par nb_sec, enleve les doublont et trier 
# outPut : un fichier avec le temps qui a été divisé par 
# 	(le nombre de jours passé en paramètre)*(le nombre de secondes en une journée)
#	et sans les doublont et trier par rapport au temps
#  	trie par rapport aux méthodes de antoine roux

if test -z "$4";then
    echo "pas de parametre: \"${4}\" "
        nb_sec=$((86400*$1))
    else
        echo "le paramètre entré est \"${4}\" "
        nb_sec=$4
fi


echo "nb_sec:$nb_sec"
awk '{printf("%s\t%s\t%s\n", int($1/'$nb_sec'), ($2>$3)?$3:$2, ($2>$3)?$2:$3)}' $2  | sort -b -nk2,2  -nk1,1 | uniq > $3
