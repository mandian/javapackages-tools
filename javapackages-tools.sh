#!/bin/sh

mav_list=
doc_list=
opt=$1
shift
while read file; do
    case "$file" in
    	*/usr/share/maven-fragments/*)
	    mav_list="$mav_list $file"	;;
    	*/usr/share/javadoc/*)
	    doc_list="$doc_list $file"	;;
    esac
done

if [ "x$mav_list" != x ]; then
    for filter in $@; do
	echo $mav_list | python /usr/lib/rpm/$filter.$opt
    done
fi
if [ $opt = req -a "x$doc_list" != x ]; then
    echo $doc_list | sh /usr/lib/rpm/javadoc.$opt
fi
