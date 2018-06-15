export PYTHONPATH=$PYTHONPATH:$PWD

#DBG="-d"

#***
# json datafile a + b + c + d 
#
if test 1 == 1;then
echo "#***"
echo "#"
cat <<EOF
bin/jsonproc $DBG   --mode=pointer-ops   json \
  'datafile(jsondata/selftest.json)' \
  '/phoneNumber/0' + '/type' + 0 + 2 

EOF
bin/jsonproc $DBG   --mode=pointer-ops   json \
  'datafile(jsondata/selftest.json)' \
  '/phoneNumber/0' + '/type' + 0 + 2 
ex=$?
echo "exit=$ex"
fi

#***
# json datafile a + b + c + d < datafile a + b
#
if test 1 == 1;then
echo "#***"
echo "#"
cat <<EOF 
bin/jsonproc $DBG --mode=pointer-ops json  'datafile(jsondata/selftest.json)' '/phoneNumber/0' + '/type' + 0 + 2 '<' 'datafile(jsondata/selftest.json)' '/phoneNumber/0' + '/type'

bin/jsonproc $DBG --mode=pointer-ops json \\
  'datafile(jsondata/selftest.json)' \\
  '/phoneNumber/0' + '/type' + 0 + 2 \\
  '<' \\
  'datafile(jsondata/selftest.json)' \\
  '/phoneNumber/0' + '/type'

EOF
bin/jsonproc $DBG   --mode=pointer-ops   json \
  'datafile(jsondata/selftest.json)' \
  '/phoneNumber/0' + '/type' + 0 + 2 \
  '<' \
  'datafile(jsondata/selftest.json)' \
  '/phoneNumber/0' + '/type'
ex=$?
echo "exit=$ex"
fi

#***
# json schemafile datafile eval( a + b + c + d < datafile a + b
#
if test 0 == 1;then
echo "#***"
echo "#"
bin/jsonproc $DBG   --mode=pointer-ops   json \
   'schemafile(jsondata/selftest.jsd)' \
   'datafile(jsondata/selftest.json)' \
   'eval(' '/phoneNumber/0' + '/type' + 0 + 2 ')' \
      '<' \
       '('
           'schemafile(jsondata/selftest.jsd)' \
           'datafile(jsondata/selftest2.json)' \
           '/phoneNumber/0' \
       ')' \
       + 
       '('
           'schemafile(jsondata/selftest.jsd)' \
           'datafile(jsondata/selftest3.json)' \
           '/type'
       ')' \
   ')'
ex=$?
echo "exit=$ex"
fi

#***
# json D0=datafile D1=datafile eval( data(D0) a + b + c + d ) < eval( data(D1) a + b )
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json 'D0' '=' 'datafile(jsondata/selftest.json)' 'D1' '=' 'datafile(jsondata/selftest.json)' 'eval(' 'data(D0)' '/phoneNumber/0' + '/type' + 0 + 2 ')' '<' 'eval(' 'data(D1)' '/phoneNumber/0' + '/type' ')'
fi

#***
# json D0=datafile D1=datafile eval( data(D0) a + b + c + d ) < eval( data(D1) a ) + b
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json 'D0' '=' 'datafile(jsondata/selftest.json)' 'D1' '=' 'datafile(jsondata/selftest.json)' 'eval(' 'data(D0)' '/phoneNumber/0' + '/type' + 0 + 2 ')' '<' 'eval(' 'data(D1)' '/phoneNumber/0' ')' + '/type' 
fi

#***
#
# json D0=datafile D1=datafile eval( data(D0) a + b + c + d ) < eval( data(D1) a ) + b
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json 'V0' '=' '(' 'datafile(jsondata/selftest.json)' '/phoneNumber/0' + '/type' + 0 + 2 ')' 'V1' '=' '(' 'datafile(jsondata/selftest.json)' '/phoneNumber/0' + '/type' ')' 'V0' '<' 'V1' 
fi

#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json 'F0' '=' 'jsondata/selftest.json' 'F1' '=' 'jsondata/selftest.json' 'datafile(F0)' '/phoneNumber/0' + '/type' + 0 + 2 '<' 'datafile(F1)' '/phoneNumber/0' + '/type'
fi


#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json '(' '/phoneNumber/0' + '/type' + 0 + 2 ')' '<' '/phoneNumber/0' + '/type'
fi

#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json '(' '/phoneNumber/0' + '/type' + 0 + 2 ')' '<' '(' '/phoneNumber/0' + '/type' ')'
fi

#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json '(' '/phoneNumber/0' + '(' '/type' + 0 ')' + 2 ')' '<' '(' '/phoneNumber/0' + '/type' ')'
fi

#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json '(' '/phoneNumber/0' + '(' '/type' + 0 ')' + 2 ')' '<' '(' '/phoneNumber/0' + '/type' ')'
fi

#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops   json 'eval(' '/phoneNumber/0' + '(' '/type' + 0 ')' + 2 ')' ')'  '<' '(' '/phoneNumber/0' + '/type' ')'
fi

#***
#
if test 0 == 1;then
bin/jsonproc $DBG   --mode=pointer-ops  json 'eval(' '/phoneNumber/0' + '(' '/type' + 0 ')' + 2 ')' ')'  '<' 'eval(' '/phoneNumber/0' + '/type' ')'
fi



exit


        Keywords - Tokens::

            '"', '\', copy, 
            schema, schemafile

            '(', ')', '"', '\', copy, eval, 
            data, datafile, schema, schemafile


       Convert the format of JSONPointer::

            input: (RFC6901,Python)
             
            output (RFC6901,Python,PythonNodeKey,JSONPointer)
        
        Pointer operations, construct a pointer::

            (+|>|<|>=|<=|==|!=)

        Pointed-Value operations::
        
            as provided by Python


      The following equivalent operation are NOT the same as the 
      previous, because they operate on the JSON data by evaluation
      of the pointed value::
                
    
      The following changes the data for evaluation::
      
        A=datafile(filename0) A=datafile(filename1) \\
          ( eval( a + b ) + eval( c ) > data(A) eval( d + ( data(B) e )
       

