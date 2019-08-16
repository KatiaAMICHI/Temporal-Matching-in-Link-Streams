#!/bin/bash

max=$1
scriptPy=$2
dir_path=$3
i=140

while [ $i -lt ${max} ]
do
  n=$(ruby -e 'puts rand(80..150)')
  t=$(ruby -e 'puts rand(350..2000)')
  d=$(ruby -e 'puts rand(1..2)')

  dir=`echo $i| awk -vvar="${dir_path}" '{printf "../res/'$dir_path'/test%04d/", $v, $0;}'`
  if [ ! -d $dir ]
  then
     mkdir $dir
  fi
  file_output="${dir}test"

  echo $n " " $t " " $d > $file_output".input"
  python3.7 $scriptPy $n $t $d >> $file_output".input"
  `cat $file_output".input" | grep -v "\[" >> $file_output".linkstream"`
  echo $n " " $t " " $d > $file_output".position"
  `cat $file_output".input" | grep "\[" >> $file_output".position"`

  i=$(expr $i + 1)

done
