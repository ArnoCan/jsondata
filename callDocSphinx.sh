PROJECT='jsondata'
VERSION="0.2.22"
RELEASE="0.2.22"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2017 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'
STATUS='alpha'
MISSION='Provide a JSON toolset for computing - RFC7159, RFC6901, RFC6902, ...'

# the absolute pathname for this source
MYPATH=${BASH_SOURCE%/*}/
if [ "X${MYPATH#.}" != "X$MYPATH" ];then
	MYPATH=${PWD}/${MYPATH#.};MYPATH=${MYPATH//\/\//\/}
fi

# input base directory
INDIR=${INDIR:-$MYPATH}
if [ "X${INDIR#.}" != "X$INDIR" ];then
	INDIR=${PWD}/${INDIR#.};INDIR=${INDIR//\/\//\/}
fi

echo "MYPATH=$MYPATH"
echo "INDIR=$INDIR"
 
# output base directory
OUTDIR=${OUTDIR:-build/}
if [ ! -e "${OUTDIR}" ];then
	mkdir -p "${OUTDIR}"
fi
export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH

# import directory for entries of static reference 
STATIC="${OUTDIR}/apidoc/sphinx/_static"

# source entities
FILEDIRS=""
FILEDIRS="${INDIR}dosrc"
FILEDIRS="$FILEDIRS ${INDIR}jsondata"
FILEDIRS="$FILEDIRS ${INDIR}bin"

#FILEDIRS="$FILEDIRS ${INDIR}UseCases"


#FILEDIRS="$FILEDIRS ${INDIR}tests"
#FILEDIRS="$FILEDIRS ${INDIR}testdata"

CALL=""
CALL="$CALL export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH;"
CALL="$CALL sphinx-apidoc "
CALL="$CALL -A '$AUTHOR'"
CALL="$CALL -H '$PROJECT'"
CALL="$CALL -V '$VERSION'"
CALL="$CALL -R '$RELEASE'"
CALL="$CALL -o ${OUTDIR}/apidoc/sphinx"
CALL="$CALL -f -F "
CALL="$CALL $@"

#
DOCHTMLDIR=${OUTDIR}apidoc/sphinx/_build/
DOCHTML=${DOCHTMLDIR}html/index.html
cat <<EOF
#
# Create apidoc builder...
#
EOF
IFSO=$IFS
IFS=';'
FX=( ${FILEDIRS} )
IFS=$IFSO
for fx in ${FX[@]};do
	echo "CALL=<$CALL '$fx'>"
	eval $CALL "$fx"
done

{
cat <<EOF 

import sys,os
sys.path.insert(0, os.path.abspath('$PWD/..'))
sys.path.insert(0, os.path.abspath('$PWD'))

html_logo = "_static/jsondata-64x64.png"
#html_favicon = None

html_theme = "default"
# html_theme = "classic"
#
#html_theme = "pyramid"
#html_theme = "agogo"
#html_theme = "bizstyle"
html_theme_options = {
#    "rightsidebar": "true",
#    "relbarbgcolor": "black",

    "externalrefs": "true",
    "sidebarwidth": "350",
    "stickysidebar": "true",
    
#    "collapsiblesidebar": "true",

#    "footerbgcolor": "",
#    "footertextcolor": "",
#    "sidebarbgcolor": "",
#    "sidebarbtncolor": "",
#    "sidebartextcolor": "",
#    "sidebarlinkcolor": "",
#    "relbarbgcolor": "",
#    "relbartextcolor": "",
#    "relbarlinkcolor": "",
#    "bgcolor": "",
#    "textcolor": "",
#    "linkcolor": "",
#    "visitedlinkcolor": "",
#    "headbgcolor": "",
#    "headtextcolor": "",
#    "headlinkcolor": "",
#    "codebgcolor": "",
#    "codetextcolor": "",
#    "bodyfont": "",
#    "headfont": "",

}

# def setup(app):
#     app.add_stylesheet('css/custom.css')
def setup(app):
	app.add_stylesheet('custom.css')

EOF
} >> ${OUTDIR}/apidoc/sphinx/conf.py
if [ ! -e "${STATIC}/css/" ];then
	mkdir "${STATIC}/css/"
fi

#
# static - literal data
#
# images
for d in docsrc/images/*.{png,jpg,gif} docsrc/*.{png,jpg,gif};do cp $d "${STATIC}"; done

# html
for d in docsrc/*.html;do cp $d "${STATIC}"; done

# txt
for d in docsrc/*.txt;do cp $d "${STATIC}"; done

# css
for d in docsrc/*.css;do cp $d "${STATIC}"; done

# py
for d in docsrc/*.py;do cp $d "${STATIC}"; done

# put the docs together
#
cat docsrc/index.rst                     > ${OUTDIR}/apidoc/sphinx/index.rst
{
cat <<EOF
**Project Data**

* PROJECT=${PROJECT}

* MISSION=${MISSION}

* AUTHOR=${AUTHOR}

* COPYRIGHT=${COPYRIGHT}

* LICENSE=${LICENSE}

* VERSION=${VERSION}

* RELEASE=${RELEASE}

* STATUS=${STATUS}

EOF
} > ${OUTDIR}/apidoc/sphinx/project.rst 

#

cp -a docsrc/*.rst "${OUTDIR}/apidoc/sphinx/"

#cp -a docsrc/myscript*.rst "${OUTDIR}/apidoc/sphinx/"
#cp -a jsondata/etc/datextime/locale/en "${STATIC}"
#cp -a jsondata/etc/datextime/locale "${STATIC}"

mkdir "${STATIC}/examples"
for d in docsrc//examples/*.py;do cp $d "${STATIC}/examples"; done

cp jsondata/data.json "${STATIC}"
cp jsondata/schema.jsd "${STATIC}"
cp jsondata/datacheck.json "${STATIC}"
cp jsondata/datacheck.jsd "${STATIC}"
cp jsondata/rfc6902.jsonp "${STATIC}"
cp jsondata/selftest.json "${STATIC}"
cp jsondata/selftest.jsd "${STATIC}"
cp jsondata/selftest.jsonp "${STATIC}"


# static - literal data
cat ArtisticLicense20.html > "${STATIC}/ArtisticLicense20.html"
cat licenses-amendments.txt > "${STATIC}/licenses-amendments.txt"
cat docsrc/profile_info.html > ${STATIC}/profile_info.html

mkdir -p ${STATIC}/examples
cp -a docsrc/examples/* ${STATIC}/examples

CALL=" "
CALL="export SPHINXBUILD=sphinx-build; "
CALL="$CALL cd ${OUTDIR}/apidoc/sphinx;"
CALL="$CALL export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH;"
CALL="$CALL make html ;"
CALL="$CALL cd - "
cat <<EOF
#
# Build apidoc...
#
EOF
echo "CALL=<$CALL>"
eval $CALL

# docdir
DOCDIR="${DOCDIR:-doc/en/html/man3/$PROJECT}"
if [ ! -e "${DOCDIR}" ];then
	mkdir -p "${DOCDIR}"
fi
# cp -a "${DOCHTMLDIR}"/html/* "${DOCDIR}"
echo
echo "display with: firefox -P preview.simple ${DOCHTML}"
echo "display with: firefox -P preview.simple ${DOCDIR}/index.html"
echo
