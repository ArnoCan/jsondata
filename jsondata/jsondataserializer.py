# -*- coding:utf-8   -*-
"""Basic features for the persistence of JSON based in-memory data.

* import and export of JSON data from/into files
* modular import and export of JSON branches from/into files
* validation by JSON schema
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys

# pylint: disable-msg=F0401
if sys.modules.get('ujson'):
    import ujson as myjson  # @UnusedImport @Reimport @UnresolvedImport
else:
    import json as myjson  # @Reimport

from jsondata import ISSTR, MS_OFF, MODE_SCHEMA_DEFAULT, \
    MATCH_NO, MATCH_KEY, MATCH_CHLDATTR, MATCH_INDEX, MATCH_MEM, \
    JSONDataError, JSONDataValueError, JSONDataModeError, \
    JSONDataSourceFileError, JSONDataTargetFileError, \
    JSONDataAmbiguityError, JSONDataParameterError, \
    mode2mj, MJ_RFC4627, MJ_DEFAULT, \
    B_ADD, B_AND, B_OR, B_XOR

from jsondata.jsondata import JSONData

import jsondata

# pylint: enable-msg=F0401


_debug = jsondata._debug  #pylint: disable=protected-access
_verbose= jsondata._verbose   #pylint: disable=protected-access


__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.21'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'


class JSONDataSerializer(JSONData):
    """Persistency for *JSONData*.
    """

    def __init__(self, jdata, **kargs):
        """Creates a serializable instance of *JSONData*, optionally loads
        and validates a JSON definition.

        Args:
            **jdata**:
                The initial data of current instance, see *JSONData*

            kargs:
                Keywords are also passed to *JSONData*.

                **datafile**:
                    Filepathname of JSON data file, when provided a further
                    search by pathlist, filelist, and filepathlist is suppressed.
                    Therefore it has to be a valid filepathname.

                **mode**:
                    The mode of JSON processing: ::

                       mode := (
                            MJ_RFC4627
                          | MJ_RFC7493  # currently not supported, mapped to RFC7159
                          | MJ_RFC7159
                          | MJ_RFC8259
                          | MJ_ECMA404  # same as RFC8259
                       )

                    default := MJ_RFC7159

                **schemafile**:
                    Filepathname of JSONschema file.

                **schema**:
                    Could be used instead of *schemafile*, see *JSONData*.

                **validator**:
                    See *JSONData*.

        Returns:
            Results in an initialized object.

        Raises:
            NameError

            JSONDataSourceFileError

            JSONDataAmbiguityError

            JSONDataValueError

            jsonschema.ValidationError

            jsonschema.SchemaError

        """
        self.debug = kargs.get('debug', _debug)
        self.verbose = kargs.get('verbose', _verbose)

        #
        self.mode_json = kargs.get('mode', MJ_DEFAULT)
        try:
            self.mode_json = mode2mj[self.mode_json]
            if self.mode_json in (MJ_RFC4627,) and type(jdata) not in (dict, list,):
                raise JSONDataModeError(
                    "mode rfc4627 requires dict or list, got:"
                    + str(type(jdata))
                    )

        except KeyError:
            raise JSONDataParameterError("Unknown mode:" + str(self.mode_json))

        #
        # data file
        #
        self.datafile = kargs.get('datafile')
        if self.datafile and not os.path.isfile(self.datafile):
            #
            # must exist when provided
            #
            raise JSONDataSourceFileError(
                "value", "datasource",
                str(self.datafile))

        #
        # schema file
        #
        self.schema = kargs.get('schema')
        self.schemafile = kargs.get('schemafile')
        if self.schemafile:
            self.schemafile = os.path.abspath(self.schemafile)
            if not os.path.isfile(self.schemafile):
                raise JSONDataSourceFileError(
                    "open", "schemafile", str(self.schemafile))

            if self.schema:
                #
                # must exist when provided
                #
                raise JSONDataAmbiguityError(
                    "value", "schema + schemafile",
                    str(self.schemafile))

            elif not os.path.isfile(self.schemafile):
                #
                # must exist when provided
                #
                raise JSONDataSourceFileError(
                    "value", "schema",
                    str(self.schemafile))

            with open(self.schemafile) as schema_file:
                self.schema = myjson.load(schema_file)
            if not self.schema:
                raise JSONDataSourceFileError(
                    "read", "schemafile", str(self.schemafile))


        validator = kargs.get('validator', MODE_SCHEMA_DEFAULT)

        #
        # load data when specified
        # use import(), for rdf7159 priitives as target too.
        # even though import requires a container as target
        #
        if type(jdata) in (list, dict):
            _j = jdata
            _k = None
        else:
            _j = []
            _k = 0

        # prepare the data container
        JSONData.__init__(
            self,
            _j,
            schema=self.schema
            )

        if self.datafile:
            if self.schema:
                self.json_import(
                    self.datafile,
                    _j,
                    _k,
                    schema=self.schema,
                    validator=validator,
                    )

            else:
                # should not be reached
                self.json_import(
                    self.datafile,
                    _j,
                    _k,
                    schemafile=self.schemafile,
                    validator=validator,
                    )

        if type(jdata) not in (list, dict):
            if _j:
                self.data = _j[0]
            else:
                self.data = None

        if self.schemafile:
            # it is the init of the creation, so initialize the schema for the object
            kargs['schemafile'] = self.schemafile
            self.set_schema(**kargs)


    def json_export(self, datafile, sourcenode=None, **kargs):
        """ Exports current data into a file.

        Args:
            **datafile**:
                File name for the exported data.

            **sourcenode**:
                Base of sub-tree for export.
                None for complete JSON document.

                default := *self.data*

            kargs:
                **force**:
                    Forces the overwrite of existing files.

                **pretty**:
                    Defines the syntax format of the data. ::

                      pretty := (
                           True     # tree view
                         | False    # all in one line
                      )

                    When set, the value is fetched from
                    *self.indent*.

                    default := *True*

        Returns:
            When successful returns 'True', else returns either 'False',
            or raises an exception.

        Raises:
            JSONDataTargetFileError:
        """
        _force = kargs.get('force')

        if kargs.get('pretty'):
            _ind = self.indent
        else:
            _ind = None

        f = os.path.abspath(os.path.normpath(datafile))
        if os.path.exists(f) and not _force:
            raise JSONDataTargetFileError("Exists, use the force to replace: " + str(f))

        if sourcenode == None:
            sourcenode = self.data

        try:
            with open(f, 'w') as fp:
                myjson.dump(sourcenode, fp, indent=_ind)
        except Exception as e:
            raise JSONDataTargetFileError("open-" + str(e), "data.dump", str(datafile))

        return True

    def json_import(self, datafile, targetnode=None, key=None, **kargs):
        """ Imports and validates data from a file.

        The schema and validator for the imported data could be set
        independent from the schema of the main data.

        Args:
            **datafile**:
                JSON data file name containing the subtree for the target branch. ::

                   datafile := <filepathname>

            **targetnode**:
                Target container for the inclusion of the loaded branch.

                .. parsed-literal::

                   targetnode := (
                       JSONPointer                  # [RFC6901]_ or [RELPOINTER]_
                       | <rfc6901-string>           # [RFC6901]_
                       | <relative-pointer-string>  # [RELPOINTER]_
                       | <pointer-items-list>       # non-URI-fragment pointer path items of [RFC6901]_
                       )

                default := *self.data*

            **key**:
                The optional index/key-hook within the *targetnode*,

                default:= None

            kargs:
                **mechanic**:
                    The import mechanic. Selects either the RFC6902 conform
                    *branch_add*, or the flexible mapping by *branch_superpose*.
                    The latter is more suitable for the application of modular 
                    templates.  ::

                       mechanic := (
                            B_ADD  |  'add'   # branch_add
                          | B_AND  |  'and'   # branch_superpose(map=B_AND)
                          | B_OR   |  'or'    # branch_superpose(map=B_OR)
                          | B_XOR  |  'xor'   # branch_superpose(map=B_XOR)
                       )


                **matchcondition**:
                    Defines the criteria for comparison of present child nodes
                    in the target container. The value is a list of criteria
                    combined by logical AND. The criteria may vary due to
                    the requirement and the type of applied container.

                **schema**:
                    JSON-Schema for validation of the subtree/branch.

                    default := *self.schema*  # the pre-loaded schema

                **schemafile**:
                    JSON-Schema filename for validation of the subtree/branch.

                    default := *self.schema*  # the pre-loaded schema

                **subpointer**:
                    The path of the sub-tree of the serialized document
                    to be imported.

                    default := ''  # whole serialized document

                **validator**:
                    Sets schema validator for the data file.
                    Current release relies on *jsonschema*, which
                    supports at the time of writing draft-03 and
                    draft-04.

                    The values are: ::

                        validator := (
                              MS_DRAFT3           | 'draft3'
                            | MS_DRAFT4           | 'draft4'
                            | MS_ON               | 'on'
                            | MS_OFF              | 'off'
                            | MODE_SCHEMA_DEFAULT | 'default'
                        )

                    default:= MS_OFF

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataError

            JSONDataValueError

            JSONDataSourceFileError:

        """
        jval = None

        schemafile = kargs.get('schemafile')
        schema = kargs.get('schema')
        subpointer = kargs.get('subpointer')

        mechanic = kargs.get('mechanic')
        _call = self.branch_superpose
        if mechanic in (B_ADD, 'add'):
            _call = self.branch_add 
#         elif mechanic in (B_AND, 'and'):
#             _call = self.branch_superpose
#         elif mechanic in (B_OR, 'or'):
#             _call = self.branch_superpose
#         elif mechanic in (B_XOR, 'xor'):
#             _call = self.branch_superpose

        matchcondition = kargs.get('matchcondition')
        if matchcondition:
            if matchcondition in ('key', MATCH_KEY):
                matchcondition.append(MATCH_KEY)
            elif matchcondition in ('no', MATCH_NO):
                matchcondition.append(MATCH_NO)
            elif matchcondition in ('child_attr_list', MATCH_CHLDATTR):
                matchcondition.append(MATCH_CHLDATTR)
            elif matchcondition in ('index', MATCH_INDEX):
                matchcondition.append(MATCH_INDEX)
            elif matchcondition in ('mem', MATCH_MEM):
                matchcondition.append(MATCH_MEM)
            else:
                raise JSONDataValueError('matchcondition', str(matchcondition))

        try:
            validator = kargs.get('validator', self.validator)
        except AttributeError:
            validator = kargs.get('validator', MODE_SCHEMA_DEFAULT)


        # INPUT-BRANCH: schema for validation
        if validator != MS_OFF:  # validation requested, requires schema
            if not schemafile:  # no new import, use present data
                if not self.schema:  # no schema data present
                    raise JSONDataError("value", "schema", self.schema)

            else:
                schemafile = os.path.abspath(schemafile)
                if not os.path.isfile(schemafile):
                    raise JSONDataSourceFileError("open", "schemafile",
                                             str(schemafile))
                with open(schemafile) as schema_file:
                    schema = myjson.load(schema_file)
                if not schema:
                    raise JSONDataSourceFileError("read", "schemafile",
                                             str(schemafile))

        # INPUT-BRANCH: data
        datafile = os.path.abspath(datafile)
        if not os.path.isfile(datafile):
            raise JSONDataSourceFileError("open", "datafile", str(datafile))
        try:
            with open(datafile) as data_file:  # load data
                jval = myjson.load(data_file)
        except Exception as e:
            raise JSONDataSourceFileError("open", "datafile", str(datafile), str(e))

        # INPUT-BRANCH: validate data
        self.validate(jval, schema, validator)

        # now - after validation - use the requested sub-branch only, default is whole branch
        if subpointer:
            jval = JSONPointer(subpointer)(jval)

        # TARGET-CONTAINER: manage new branch data
        if isinstance(targetnode, JSONData):
            return _call(jval, targetnode.data, key)
        elif type(targetnode) in (dict, list):
            return _call(jval, targetnode, key)
        elif isinstance(targetnode, JSONPointer):
            return _call(jval, targetnode, key)
        elif type(targetnode) in ISSTR:
            return _call(jval, targetnode, key)
        elif targetnode == None:
            if self.data != None:
                return _call(jval, self.data)
            return _call(jval, '')

#         if isinstance(targetnode, JSONData):
#             return self.branch_add(jval, targetnode.data, key)
#         elif type(targetnode) in (dict, list):
#             return self.branch_add(jval, targetnode, key)
#         elif isinstance(targetnode, JSONPointer):
#             return self.branch_add(jval, targetnode, key)
#         elif type(targetnode) in ISSTR:
#             return self.branch_add(jval, targetnode, key)
#         elif targetnode == None:
#             if self.data != None:
#                 return self.branch_add(jval, self.data)
#             return self.branch_add(jval, '')

        raise JSONDataParameterError("import requires a container: object(dict) or array(list).")


    def dump_data(self, pretty=True, **kargs):
        """Dumps structured data by calling *json.dumps()*.

        Args:
            **pretty**:
                Activates pretty printer for treeview, else flat.

            kargs:
                The remaining keyword arguments are passed 
                through to *json.dumps()*.

                **ensure_ascii**:
                    See *json_dumps*.
                    
                    default := False

                **indent**:
                    Sets indent when *pretty* is *True*.

                **sort_keys**:
                    Sorts keys.

                    default := False

                **sourcefile**:
                    Loads data from 'sourcefile' into 'source'.

                    default := None

                **source**:
                    Prints data within 'source'.

                    default := self.data

        Returns:
            When successful returns the dump string, else either 'None', 
            or raises an exception.

        Raises:
            JSONDataAmbiguityError:

            forwarded from 'json'

        """
        try:
            source = kargs.pop('source')
        except KeyError:
            source = None
 
        try:
            sourcefile = kargs.pop('sourcefile')
        except KeyError:
            sourcefile = None

        if sourcefile and source:
            raise JSONDataAmbiguityError('sourcefile/source',
                                         "sourcefile=" + str(sourcefile),
                                         "source=" + str(source))
        if sourcefile:
            source = open(sourcefile)
            source = myjson.load(source)
        elif not source:
            source = self.data  # yes, almost the same...

        if not kargs.get('indent') and pretty:
            kargs['indent'] = self.indent
        if not kargs.get('ensure_ascii'):
            kargs['ensure_ascii'] = False
        # if not kargs.get('sort_keys'):
        #   kargs['sort_keys'] = False
        
        return myjson.dumps(source, **kargs)


    def dump_schema(self, pretty=True, **kargs):
        """Dumps structured schema by calling *json.dumps()*.

        Args:
            **pretty**:
                Activates pretty printer for treeview, else flat.

            kargs:
                The remaining keyword arguments are passed 
                through to *json.dumps()*.

                **ensure_ascii**:
                    See *json_dumps*.
                    
                    default := False

                **indent**:
                    Sets indent when *pretty* is *True*.

                **sort_keys**:
                    Sorts keys.

                    default := False

                **sourcefile**:
                    Loads schema from 'sourcefile' into 'source'.

                    default := None

                **source**:
                    Prints schema within 'source'.

                    default := self.schema

        Returns:
            When successful returns the dump string, else either 'None',
            or raises an exception.

        Raises:
            JSONDataAmbiguityError:

            forwarded from 'json'

        """
        try:
            source = kargs.pop('source')
        except KeyError:
            source = None
 
        try:
            sourcefile = kargs.pop('sourcefile')
        except KeyError:
            sourcefile = None

        if sourcefile and source:
            raise JSONDataAmbiguityError('sourcefile/source',
                                         "sourcefile=" + str(sourcefile),
                                         "source=" + str(source))
        if sourcefile:
            source = open(sourcefile)
            source = myjson.load(source)
        elif not source:
            source = self.schema  # yes, almost the same...

        if not kargs.get('indent') and pretty:
            kargs['indent'] = self.indent
        if not kargs.get('ensure_ascii'):
            kargs['ensure_ascii'] = False
        # if not kargs.get('sort_keys'):
        #     kargs['sort_keys'] = False
        return myjson.dumps(source, **kargs)


    def set_schema(self, schemafile=None, targetnode=None, **kargs):
        """Sets schema or inserts a new branch into the current schema.
        The main schema(targetnode==None) is the schema of the current
        instance. Additional branches could be added by importing the
        specific schema definitions. These could either kept volatile
        as a temporary runtime extension, or stored persistently.

        Args:
            **schemafile**:
                JSON-Schema filename for validation of the
                subtree/branch, see also *kargs['schema']*.

            **targetnode**:
                Target container hook for the inclusion of
                the loaded branch.

            kargs:
                **schema**:
                    In-memory JSON-Schema as an alternative
                    to schemafile, when provided the 'schemafile'
                    is ignored.

                    default:=None

                **persistent**:
                    Stores the 'schema' persistently into 'schemafile'
                    after the completion of update, requires a
                    valid 'schemafile'.

                    default:=False

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:

            JSONDataError

            JSONDataSourceFileError

            JSONDataValueError

        """
        schema = kargs.get('schema')
        persistent = kargs.get('persistent', False)

        if schemafile:
            self.schemafile = schemafile
        elif self.schemafile != None:  # use present
            schemafile = self.schemafile

        if not schemafile:
            if persistent:  # persistence requires storage
                raise JSONDataTargetFileError("open", "JSONSchemaFilename",
                                         schemafile)

        if schemafile:  # load from file
            schemafile = os.path.abspath(schemafile)
            self.schemafile = schemafile
            if not os.path.isfile(schemafile):
                raise JSONDataSourceFileError("open", "schemafile", str(schemafile))
            with open(schemafile) as schema_file:
                schema = myjson.load(schema_file)
            if schema == None:
                raise JSONDataSourceFileError("read", "schemafile", str(schemafile))

        else:  # missing at all
            raise JSONDataSourceFileError("open", "schemafile", str(schemafile))

        #
        # manage new branch data
        #
        if not targetnode:
            self.schema = schema

        else:  # data history present, so decide how to handle

            # the container hook has to match for insertion-
            if type(targetnode) != type(schema):
                raise JSONDataError(
                    "type", "target!=branch",
                    str(type(targetnode)) + "!=" + str(type(schema)))

            self.branch_add(schema, targetnode, None)

        return schema != None


from jsondata.jsonpointer import JSONPointer
# avoid nested recursion problems
