#!/bin/sh

#sets dir to directory containing this script
dir=`dirname $0`

#use $dir/ as prefix to run any programs in this dir
#so that this script can be run from any directory.

#ls $dir/pySol

python3 $dir/pySol/main.py

if [ $? -ne 0 ];
then
  exit 1
else
  exit 0
fi 
#com
