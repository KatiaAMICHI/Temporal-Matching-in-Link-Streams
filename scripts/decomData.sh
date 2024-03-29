#! /bin/bash

# $1 >> nb days
# $2 >> input file
# $3 >> output file
# $4 >> nb_sec pour décomposer

# devise le temps par nb_sec, enleve les doublont et trier 
# outPut : un fichier avec le temps qui a été divisé par 
# 	(le nombre de jours passé en paramètre)*(le nombre de secondes en une journée)
#	et sans les doublont et trier par rapport au temps
# si $1 == 0 alors on n'éffectue pas de décompo juste le trie


if test -z "$4";then
    echo "pas de parametre: \"${4}\" "
	if test $1 -eq 0
        then
        nb_sec=1
	else
            nb_sec=$((86400*$1))
	fi
else
    echo "le paramètre entré est \"${4}\" "
	nb_sec=$4
fi


echo "nb_sec:$nb_sec"
awk '{printf("%s\t%s\t%s\n", int($1/'$nb_sec'), ($2>$3)?$3:$2, ($2>$3)?$2:$3)}' $2  | sort -n | uniq > $3

