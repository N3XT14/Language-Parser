#!/bin/sh

extras=$HOME/cs571/projects/prj1/extras
dir=$HOME/i571/submit/prj1-sol

if [ -z "$1" ]
then
	$extras/do-tests.sh $dir/decls.sh
else
	$extras/do-tests.sh $dir/decls.sh $extras/tests/$1
fi
	
