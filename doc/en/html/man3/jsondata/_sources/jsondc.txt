jsondc
#############

The *jsondc* commandline interface provides access to several 
tasks of the *jsondata* package, which internally rely on the standard 
packages 'json' and 'jsonschema'.
It offers access to the API of the classes and provides a selftest
option for the quick verification of the package state.
The runtime contained selftest class including it's test data serve
as an example in addition to the unit test data.

The interface provides a callable generic validator(default:=Draft4) for arbitrary
JSON data files. The validation is performed with a main JSON schema file linking 
additional sub-configuration for an optional set of an arbitrary number of branches.
It provides the validation of JSON based data/files by their corresponding JSONschemas.
The call interface is Linux/Unix command line standard - on other supported OS too - 
with a few conventions related to default values of file names and paths.

The application of this call interface is mainly intended for the purposes:

1. as a developer utility for the development of JSON based data

2. as a user tool in order to enumerate the list of actually 
   used JSON sources

3. as a user tools in order to verify the present JSON data

4. as a automation and test tool for various JSON specifications,
   and JSON based applications

5. as a selftest and environment verification for the processing
   of complex JSON data.
 
Therefore the assembly of data tree models with basic branch functions 
in accordance/complance to RFC6901 and RFC6902 is provided for the 
incremental setup, continous modification, and serialization of JSON data.

When no explicit filenames are provided the following convention is applied
as default::

    appname: "-a"
        "JSONobjects"

    JSON-schema: "-s"
        dirname(__file__)/<appname>.jsd ("jsondata.jsd")

    JSON-data: "-c"
        <appname>.json ("jsondata.json")

    Search-path-data: "-p"
        Search path for JSON-data - refer to __file__=JSONData/Serializer.py:
        default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/

**SYNOPSIS:**::

  jsondc [OPTIONS]

**OPTIONS:**::
  -a --appname= <appname>
     Name of application.
     default: jsondc
  -c --configfile= <configfile>
     A single configuration file including path with JSON data.

     default: jsondc.json
  -D --print-data
     Pretty print data.
  -d --debug
     Debug entries, does NOT work with 'python -O ...'.
     Developer output, aimed for filtering.
  -f --filelist= <list-of-filenames>
     List of colon seperated filenames to be searched for. These 
     could be relative pathnames too.

     default:=[<appname>.json]
  -h --help
     This help.
  -i --interactive
     Dialog mode, displays formatted for interactive JSON and 
     JSONschema design.
  -n --no-default-path
     Supress load of default path.

     default: False
  -N --no-sub-data
     Supress load of sub-data files, e.g. from plugins.

     default: False
  -p --pathlist= <search-path-JSON-data>
     Search path for JSON data file(s), standard list for current platform.

     default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
  -P --plugins-pathlist= <search-path-JSON-data-branches>
     Search path for JSON data file(s) to be inserted as additional branches,
     standard list for current platform.

     default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
  -s --schemafile= <schemafile>
     Schema file - JSONschema.

     default: jsondc.jsd
  -S --print-schema
     Pretty print schema.
  -selftest --selftest

     Performs a basic functional selftest by load, verify, and validate.

     0. jsondata/data.json + jsondata/schema.jsd
     1. jsondata/selftest.json + jsondata/selftest.jsd

  -V --validator= <validator>
     Alternate validator provided by module 'jsonschema'
     - default: validate
     - draft3: Draft3Validator
     - off: None

    default:= validate
  -Version --Version
     Current version - detailed.
  -v --verbose
     Verbose, some relevant states for basic analysis.
     When '--selftest' is set, repetition raises the display level.
  -version --version
     Current version - terse.

**ENVIRONMENT**::
  * PYTHON OPTIONS:
    -O, -OO: Eliminates '__debug__' code.
 
