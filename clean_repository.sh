#!/bin/bash

# clean the test results
cd tests
python clean_tests.py >/dev/null 2>/dev/null
cd -

# remove all .pyc files
pyclean .
rm -rf *~

# rm this silly file
rm -f test/ins_rec_model/Working_Folder/Rplots.pdf

