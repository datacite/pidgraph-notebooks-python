#!/usr/bin/env bash
# For each user-story-*/*-with-output.ipynb notebook, this script generates two files: 1. 'no output jupyter notebook' and 2. 'with output html'
for jn in $(ls user-story-*/*-with-output.ipynb); do
    no_output_jn=`echo $jn | perl -p -e 's|\-with\-output||'`
    echo "About to convert $jn to $no_output_jn"
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to notebook --stdout $jn > $no_output_jn
done
