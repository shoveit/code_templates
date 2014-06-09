awk '{if(NR==1)sub(/^\xef\xbb\xbf/,"");print}' $1 > t
mv t $1
