#!/bin/bash

DATA_ROOT_DIR=$1

CURRENT_DIR=`pwd`

cd $DATA_ROOT_DIR 

for f in `find . -type f -name "*.tgz"`; do 
  d=`dirname $f`
  fl=`basename $f`
  (cd $d && tar zxvf $fl)
  (cd $d && rm $fl)
done
