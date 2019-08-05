#!/bin/sh

max=$1
i=1

while [ $i -lt $max ]
do
  n=$(ruby -e 'puts rand(5..7)')
  t=$(ruby -e 'puts rand(5..7)')
  d=$(ruby -e 'puts rand(1..3)')
  file_output=`echo $i| awk '{printf "tests/test%04d", $0;}'`
  echo $n " " $t " " $d > $file_output".input"
  python gen1D.py $n $t $d >> $file_output".input"
  i=$(expr $i + 1)
  `cat $file_output".input" | grep -v "\[" > $file_output".linkstream"`  
  echo $n " " $t " " $d > $file_output".position"
  `cat $file_output".input" | grep "\[" >> $file_output".position"`
done
