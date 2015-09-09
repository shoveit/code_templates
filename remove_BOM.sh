# 0. perl
perl -i -CD -pe 'tr/\x{feff}//d' *.txt

# 1.
awk '{if(NR==1)sub(/^\xef\xbb\xbf/,"");print}' $1 > t
mv t $1



# 2. Gnu sed, Removing BOM from all text files in current directory:
sed -i '1 s/^\xef\xbb\xbf//' *.txt


# 3. FreeBSD/OS X sed,
sed -i .bak '1 s/^\xef\xbb\xbf//' *.txt


