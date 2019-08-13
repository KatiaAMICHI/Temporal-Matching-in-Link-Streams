#!/bin/sh

max=$1
i=1

while [ $i -lt ${max} ]
do
  n=$(ruby -e 'puts rand(8..15)')
  t=$(ruby -e 'puts rand(7..10)')
  d=$(ruby -e 'puts rand(1..3)')

  dir=`echo $i| awk '{printf "../res/gen_test/test%04d/", $0;}'`
  if [ ! -d $dir ]
  then
     mkdir $dir
  fi
  file_output="${dir}test"
  echo $n " " $t " " $d > $file_output".input"
  python3.7 gen1D.py $n $t $d >> $file_output".input"
  i=$(expr $i + 1)
  `cat $file_output".input" | grep -v "\[" > $file_output".linkstream"`  
  echo $n " " $t " " $d > $file_output".position"
  `cat $file_output".input" | grep "\[" >> $file_output".position"`
done
