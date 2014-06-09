#!/bin/bash
# Uniq input $file into $file.uniq then count record by column number.
# Usage: bash $0 'file-pattern'
# Example: bash $0 '*.sample'
# Date: Mon Jun  9 23:36:43 HKT 2014
# Contact: yuqiulin496@pingan.com

for i in `ls $1` ; do 
	awk '!a[$0]++' $i > $i.uniq
	echo "---$i.uniq---"
	echo "NF	cnt"
	awk -F"\t" 'BEGIN{OFS="\t"}{a[NF]++}END{for(i in a){print i,a[i]}}' $i.uniq | sort -k2nr
done 
