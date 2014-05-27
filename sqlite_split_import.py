#!/usr/bin/env python
#encoding=utf-8
import sys,os,re
import getopt
import sqlite3
from subprocess import PIPE,Popen

FILE_PATH = os.path.realpath(os.path.dirname(__file__))

#------ usage
def usage():
	print '''
		Split file into in-RAM chunks & import into sqlite3 DB
		Modify your own import_func.
		Usage: python $0 -d pingan.db --separator='\x01' -t weibo_user weibo_user.txt
		Contact: qiulin.work@gmail.com
		Date: Fri Mar 14 14:09:23 HKT 2014
		'''

#------ split file
def split_import(filename,import_func,chunk_size_line=5000):
	chunk = []
	with open(filename) as F:
		for lineno, line in enumerate(F):
			if lineno % chunk_size_line == 0:
				if len(chunk)>0:
					import_func(chunk)
					chunk = []
                        try:
                            chunk.append(line.strip().decode('utf-8'))
                        except:
                            pass # decode error,shit just happens.
		if len(chunk)>0: #  final chunk
			import_func(chunk)

#------ import_func defination, modify your own here
def import_table(records):
	'''
	input a list of unicode record strings. split each into fileds then import to database.
	'''
	global separator,cur,tablename
	field_cnt = len(cur.execute('PRAGMA table_info(%s)' % tablename).fetchall())
	placeholders = ','.join(('?',)*field_cnt)
	import_sql_template = 'INSERT INTO %s VALUES (%s)' % (tablename,placeholders)
	splitted = map(lambda x:tuple(x.split(separator)),records)
	splitted = filter(lambda x:len(x) == field_cnt,splitted)
#debug:        print map(lambda x:len(x), splitted)
        cnt = 0
        for i in splitted:
            try:
                cur.execute(import_sql_template,i)
            except:
                cnt +=1
#only lucky:	cur.executemany(import_sql_template,splitted)
        print '%i has been imported\n' % (len(splitted) - cnt)


if __name__ == "__main__":
	#---------- initial
	sqlite_db = None
	separator = '\t'
	#----------- opts parser
	opts,args = getopt.getopt(sys.argv[1:], "hd:t:s:", ["help","db=","table=","separator="])
		
	for (k,v) in opts:
		if k in ("-h","--help"):
			usage()
			sys.exit()
		if k in ("-s","--separator"):
			separator = v
		if k in ("-d","--db"):
			sqlite_db = v
		if k in ("-t","--table"):
			tablename = v
	
	if sqlite_db is None:
		print "Pls specify a sqlite database"
		usage()
		sys.exit()
	if len(args) == 0:
		print "No input file"
		usage()
		sys.exit()
	filename=args[0]

	#-- DB connect
	conn = sqlite3.connect(sqlite_db)
	cur = conn.cursor()
	cur.execute('PRAGMA journal_mode=memory')
	cur.execute('PRAGMA synchronous=0')
	cur.execute('PRAGMA cache_size=1500000')

        #-- split & import
	split_import(filename,import_table)
	conn.commit()
	conn.close()
