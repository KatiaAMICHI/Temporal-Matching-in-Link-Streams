#!/bin/bash
# TODO lancer le script 300 fois, puis lancer celui de sort AR
max=$1
scriptPy=$2
dir_path=$3
i=900
# 370 -> 1500
  # n=$(ruby -e 'puts rand(20..50)')
  # t=$(ruby -e 'puts rand(50..150)')
  # d=$(ruby -e 'puts rand(1..2)')

# 0 -> 299
  # n=$(ruby -e 'puts rand(20..40)')
  # t=$(ruby -e 'puts rand(20..50)')
  # d=$(ruby -e 'puts rand(1..2)')

# 300 -> 599
  # n=$(ruby -e 'puts rand(40..60)')
  # t=$(ruby -e 'puts rand(50..75)')
  # d=$(ruby -e 'puts rand(1..2)')

# 600 -> 899
  # n=$(ruby -e 'puts rand(60..90)')
  # t=$(ruby -e 'puts rand(75..100)')
  # d=$(ruby -e 'puts rand(1..2)')

# 900 -> 950
while [ $i -lt ${max} ]
do
   n=$(ruby -e 'puts rand(90..120)')
   t=$(ruby -e 'puts rand(100..200)')
   d=$(ruby -e 'puts rand(1..2)')
#  n=6
#  t=11
#  d=1
  dir=`echo $i| awk -vvar="${dir_path}" '{printf "../res/'$dir_path'/test%04d/", $v, $0;}'`
  if [ ! -d $dir ]
  then
     mkdir $dir
  fi
  file_output="${dir}test"

  echo $n " " $t " " $d > $file_output".input"
  python3.7 $scriptPy $n $t $d >> $file_output".input"
  `cat $file_output".input" | grep -v "\[" > $file_output".linkstream"`
  echo $n " " $t " " $d > $file_output".position"
  `cat $file_output".input" | grep "\[" >> $file_output".position"`

  i=$(expr $i + 1)

done
