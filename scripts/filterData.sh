#! /bin/bash

# intPut
# 	$1 >> nb days
# 	$2 >> input file
# 	$3 >> output file
#   $4 >> paramètre pour indiqué si c'est en seconde ou en jours (si on a déja fait passé le fichier par le script decomData) (s >> seconde et d >> days)

# outPut 
# 	plusieurs fichiers découper par rapport au nombre de jours passer en paramètre


echo " le nb d'arg:$#"
if [ "$#" -ne 4 ]; then
     echo "Le nombre d'arguments est invalide"
else
    if [ ! -d "../res/filterDataEnron" ];then
        echo "Création du dosser filterDataEnron !";
        mkdir ../res/filterDataEnron
    fi

    echo "':>> $4"
    var_sec_days=1
    if [ $4 = "s" ]; then
        var_sec_days=86400
    fi

    echo "var_sec_days:$var_sec_days"
    nb_sec=$((var_sec_days*$1))
    echo "nb_sec:$nb_sec"
    beg=0
    end=$((var_sec_days*$1))

    while read line
    do
        t=`echo $line | cut -d' ' -f 1`;
        if (( t >= end ))
        then
            beg=$end
            end=$((end+nb_sec))
        fi

        fileout="../res/filterDataEnron/"$3"_$((beg/var_sec_days))_$((end/var_sec_days))"
        echo -e "$line  " >> $fileout
    done < $2
fi