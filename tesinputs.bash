#!/bin/bash

pattern='([[:digit:]])'

inputs=$@
count=0
for input in ${inputs[*]}; do
   echo INPUT=$input
   models[$count]=$input
   echo model=${models[$count]}
   dummy=$input
   ((count++))
done
echo incount=$count
dummodel=${models[@]:0:$((count-1))}

echo DUMMODEL=$dummodel
obtype=$dummy
echo OBTYPE=$obtype
unset models
models=$dummodel


echo models=${models}
echo obtype=$obtype





