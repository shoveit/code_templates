#!/usr/bin/bash
# this is a one-liner to get record-count from sqlite3 DB.
# Usage: bash $0 DB table-name-regexp
for tab in `sqlite3 $1 '.tables'`;do echo $tab;sqlite3 $1 "select count(*) from $tab";done|egrep $2 -A 1
