#!/bin/bash

#need to repeat until 999 is small
csplit -n 3 ipg160105.xml /xml/ {9999999}

#for i in `seq 000 1 998`
#do
#python add_database.py xx{i}
#done
