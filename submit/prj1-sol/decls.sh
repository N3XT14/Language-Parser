#!/bin/sh

#sets dir to directory containing this script
dir=`dirname $0`

#use $dir/ as prefix to run any programs in this dir
#so that this script can be run from any directory.

#ls $dir/pySol

python3 $dir/pySol/main.py

#<< com
#echo $?
#RETURN=$?
#echo $RETURN
#echo $?
if [ $? -ne 0 ];
then
  #echo "The script myscript.sh was executed successfuly"
  exit 1
else
  #echo "The script myscript.sh was NOT executed successfuly and returned the code $RETURN"
  exit 0
fi 
#com
