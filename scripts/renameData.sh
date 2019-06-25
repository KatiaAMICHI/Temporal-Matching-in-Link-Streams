#! /bin/bash

# inPut:
# 	$1 >> nb_element (valeur max d'un element)
# 	$2 >> input file name
# 	$3 >> output file name

#outPut
# 	le output_file où tous les noeuds sont renomé

nb_element=100000

declare -A my_array
i=0

# TODO si y a un moyen de vérifier si un element n'est pas encore inisiatlisé dans un tableau comme ça pas besoin de tt parcourir 
while ((i < $1))
do
	my_array+=([$i]=-1)
	((i++))	
done

var=0
while read line
do	
	t=`echo $line | cut -d' ' -f 1`;
	a=`echo $line | cut -d' ' -f 2`;
	b=`echo $line | cut -d' ' -f 3`;
	
	if [ "${my_array[$a]}" == -1 ]; then
		my_array[$a]=$var
		((var++))
	fi
	if [ "${my_array[$b]}" == -1 ]; then
		my_array[$b]=$var
		((var++))
	fi
	echo -e "$t\t${my_array[$a]}\t${my_array[$b]}" >> $3	
done < $2

