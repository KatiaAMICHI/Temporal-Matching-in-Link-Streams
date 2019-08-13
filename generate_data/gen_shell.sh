#!/bin/sh

max=$1
i=0

while [ $i -lt ${max} ]
do
  n=$(ruby -e 'puts rand(80..150)')
  t=$(ruby -e 'puts rand(350..2000)')
  d=$(ruby -e 'puts rand(1..2)')

  dir=`echo $i| awk '{printf "../res/gen_B1/test%04d/", $0;}'`
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
