#!/usr/bin/bash

#this script compiles the given code (as required by the language) and executes it
#first cl argument	$1: the programming language that the code is written in
#second cl argument	$2: the file with the program

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
