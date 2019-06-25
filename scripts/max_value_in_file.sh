#! /bin/bash

# pour trouver la valeur max dans un fichier 

#input :	$1 : input file
# outPut :	la line qui a le valeur max


sort -n -u -k2 $1 | tail -1
sort -n -u -k2 $1 | tail -1 
