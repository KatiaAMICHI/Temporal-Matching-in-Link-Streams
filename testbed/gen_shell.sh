#!/bin/sh

max=$1
i=1

while [ $i -lt $max ]
do
  n=$(ruby -e 'puts rand(5..7)')
  t=$(ruby -e 'puts rand(5..8)')
  d=$(ruby -e 'puts rand(1..1)')
  file_output="tests/test"$n"_"$t"_"$d
  echo $n " " $t " " $d > $file_output".input"
  python gen1D.py $n $t $d >> $file_output".input"
  i=$(expr $i + 1)
  `cat $file_output".input" | grep -v "\[" > $file_output".linkstream"`  
  echo $n " " $t " " $d > $file_output".position"
  `cat $file_output".input" | grep "\[" >> $file_output".position"`
done
