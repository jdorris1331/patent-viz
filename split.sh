#!/bin/bash


csplit -n 4 -k ipg160105.xml /xml/ {9999999}

#python add_database.py ${PREFIX}{i}

