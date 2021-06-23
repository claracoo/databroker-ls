#!/bin/bash
python qt.py
while [ true ] ; do
read -s -n1 input
if [ "$input" = $'\e' ] ; then
exit ;
else
echo "woo"
fi
done