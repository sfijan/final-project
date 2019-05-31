#!/usr/bin/bash

if [ "$1" == "python 2.7" ]
then
    python2.7 $2
elif [ "$1" == "python 3.7" ]
then
    python3.7 $2
elif [ "$1" == "c" ]
then
    gcc $2
    ./a.out
fi
