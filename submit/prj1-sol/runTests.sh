#!/bin/sh

extras=$HOME/cs571/projects/prj1/extras


if [ -z "$1" ]
then
	$extras/do-tests.sh decls.sh
else
	$extras/do-tests.sh decls.sh $extras/tests/$1
fi
	
