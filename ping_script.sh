#!/bin/sh

#echo $1 >> $3
#echo $2 >> $3
#echo $3 >> $3
ping $1 $2 $3 > $4 2>&1
echo "Ok" >> $4