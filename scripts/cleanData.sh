#! /bin/bash

# inPut :
#	$1 : fichier entrant	 
#	$2 : fichier sortant

# outPut :
# 	fichier sans doublant, et la variable temps à la première place


awk '{printf("%s\t%s\t%s\n", $3, ($1>$2)?$2:$1, ($1>$2)?$1:$2)}' $1 | tac > $2
