#!/bin/sh

mvn_list=
osg_list=
doc_list=
opt=$1
export RPM_BUILD_ROOT=$2
builddir=$3
while read file; do
    case "$file" in
    	*/usr/share/maven-metadata/*)
	    mvn_list="$mvn_list $file"	;;
	*.jar|*/MANIFEST.MF)
	    osg_list="$osg_list $file"	;;
    	*/usr/share/javadoc/*)
	    doc_list="$doc_list $file"	;;
    esac
done

if [ "x$mvn_list" != x ]; then
    echo $mvn_list | sed 's/ /\n/g' | python /usr/lib/rpm/maven.$opt $builddir
fi
if [ "x$osg_list" != x ]; then
    echo $osg_list | sed 's/ /\n/g' | python /usr/lib/rpm/osgi.$opt $builddir
fi
if [ $opt = req -a "x$doc_list" != x ]; then
    echo $doc_list | sed 's/ /\n/g' | python /usr/lib/rpm/javadoc.$opt
fi
