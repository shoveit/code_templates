#!/usr/bin/env bash
# Usage: bash $0 xxx.db model_name
# Delete all indexes in a sqlite3 database. I use this to drop index before import massive data into tables, this can speed up dramaticly by avoiding indexing at run-time.

for i in  `sqlite3 $1 "select name from sqlite_master where type='index' and name like '$2%';"`;
do
echo $i;
sqlite3 $1 "drop index $i";
done
