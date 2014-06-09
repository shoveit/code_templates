#!/usr/bin/python 
help= """
Input a file group by a certain field, collect records one-by-one and proceed group every time a new ID emergs.

Usage: cat timelines_group_by_uid.txt | python $0 

Example1: print first column
cat test.data |python $0 --flag="map" --lambda="x:split()[0]"

Example2: print if first column > 10
cat test.data |python $0 --flag="filter" --lambda="x:int(x.split()[0])>10"

Example3: print if second column containing a '2'
cat test.data |python $0 --flag="filter" --lambda="x:'2' in x"
Contact: yuqiulin496@pingan.com
Date: Mon Mar 24 16:09:34 CST 2014
"""

import os,sys

def proceed_group(flag,LAMBDA,records):
	if len(records) == 0: 
		return ["log:blank group:%s" % records]
	if len(records) < 2 and flag == "reduce":
		return ["log:single line:%s" % records]
	
	func_template = "%s(lambda %s,%s)" % (flag,LAMBDA,"LIST")
	LIST=records
	return eval(func_template)

if __name__=="__main__":
	import getopt

	opts,args = getopt.getopt( sys.argv[1:], "hF:L:", ["help","flag=","lambda="])

	for (k,v) in opts:
		if k in ("-L","--lambda"):
			LAMBDA = v
		if k in ("-F","--flag"):
			flag = v
		if k in ("-h","--help"):
			sys.exit(help)

	current_records = []
	current_id = 'never-seen'
	for line in sys.stdin:
		id = line.split()[0]	
		if current_id == id:
			current_records.append(line.strip())
		else:
			group_result = proceed_group(flag,LAMBDA,current_records)
			print '\n'.join(map(str,group_result))
			current_id = id
			current_records = [line.strip()]

