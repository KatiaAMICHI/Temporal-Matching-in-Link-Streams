#!/bin/bash
max=$1
scriptPy=$2
dir_path=$3
i=0

while [ $i -lt ${max} ]
do
   n=$(ruby -e 'puts rand(20..200)')
   t=$(ruby -e 'puts rand(20..200)')
   d=$(ruby -e 'puts rand(1..10)')

  dir=`echo $i| awk -vvar="${dir_path}" '{printf "../res/'$dir_path'/test%04d/", $v, $0;}'`
  if [ ! -d $dir ]
  then
     mkdir $dir
  fi
  file_output="${dir}test"
  # l=`cat $file_output".linkstream" | wc -l`
  l=1000000000000
  if (( l > 30000 )); then
      echo "$file_output: $l"
      echo $n " " $t " " $d > $file_output".input"
      python3.7 $scriptPy $n $t $d >> $file_output".input"
      `cat $file_output".input" | grep -v "\[" > $file_output".linkstream"`
      echo $n " " $t " " $d > $file_output".position"
      `cat $file_output".input" | grep "\[" >> $file_output".position"`
      l=`cat $file_output".linkstream" | wc -l`
        if (( l > 190000 )); then
            i=$(expr $i - 1)
        fi

       echo "FIN  $file_output: $l"
  fi
  i=$(expr $i + 1)

done
