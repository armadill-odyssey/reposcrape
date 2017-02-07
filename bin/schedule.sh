#!/bin/bash

DIR=$HOME/Developer/School/CSC3130/reposcrape

cd $DIR
source ./venv/bin/activate

python ./main.py

deactivate
