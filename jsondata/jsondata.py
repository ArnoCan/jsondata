# -*- coding:utf-8   -*-
"""Core features for the processing of JSON based structures of in-memory data.
Supports RFC4627 and RCF7159, addresses of in-memory-nodes and RFC6901, 
relative pointer-draft.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys
import re

import copy

#
# pylint: disable-msg=F0401
if sys.modules.get('ujson'):
    import ujson as myjson  # @UnusedImport @Reimport @UnresolvedImport
else:
    import json as myjson  # @Reimport
# pylint: enable-msg=F0401

# for now the only one supported
import jsonschema
from jsonschema import ValidationError as JSONDataValidationError
from jsonschema import SchemaError as JSONDataSchemaError

from jsondata import V3K, ISSTR

from jsondata import JSONDataParameterError, JSONDataError, \
    JSONDataValueError, JSONDataIndexError, JSONDataKeyError, \
    JSONDataSourceFileError, JSONDataTargetFileError, \
    JSONDataNodeTypeError, JSONPointerError, JSONPointerTypeError, \
    JSONDataPathError, \
    MJ_RFC4627, MJ_RFC7159, MJ_RFC6901, \
    MJ_RFC6902, MS_OFF, MS_DRAFT3, MS_DRAFT4, \
    C_REF, C_DEEP, C_SHALLOW, \
    C_DEFAULT, \
    PJ_TREE, PJ_FLAT, PJ_PYTREE, PJ_PYFLAT, PJ_REPR, PJ_STR, \
    JSYN_NATIVE, JSYN_PYTHON, \
    validator2ms, copy2c, mode2mj, \
    B_AND, B_OR, B_XOR # B_MOD #B_SUB, B_MULT, B_DIV

__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez" \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.21'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

if V3K:
    unicode = str


class JSONpl(list):
    """A wrapper for a 'list' representing a path pointer
    at the method interfaces. Required due to possible
    ambiguity with the other type of in-memory node.
    """
    pass


class JSONData(object):
    """ Representation of a JSON based object data tree.

    The common node address parameters are defined as: ::

       sourcenode := <commonnode>|<indata> # depends on the interface

       targetnode := <innode>              # target within the represented
                                           # JSON structure

       commonnode := (anydata | indata)

       anydata  := (                       # any data hook - within
                                           # self.data or external
           JSONData                        # - adds to the contained data
                                           #   of the reference
         | <json-array-list>               # - adds to JSON array
         | <json-object-dict>              # - adds to JSON object
       )

       indata := (                         # within self.data
           JSONPointer                     # - adds to the node within
                                           #   self.data [RFC6901]_
         | <rfc6901-string>                # - pointer string within self.data [RFC6901]_
         | <relative-pointer-string>)      # - relative pointer within self.data [RELPOINTER]_
       )

    **REMARK**:
        The RFC7159 permits any JSON type as a node, while the RFC4627
        permits array and object as node reference only.
    """

    def __init__(self, jdata, **kargs):
        """Creates and validates a new object from the provided JSON data.
        Arbitrary additional JSON data could be added as branches.

        Args:
            **jdata**:
                The initial data of current instance. The accepted formats
                are in-memory representation of JSON data compatible with
                the standard library *json* [json]_. The permitted input
                types vary in accordance to the selected operations mode
                of either *RFC4627* or *RFC7159*. ::

                   type(jdata) := (
                        list,       # json-array
                      | dict,       # json-object
                      | JSONData    # copy constructor
                      | int         # RFC7159 only
                      | float       # RFC7159 only
                      | unicode     # RFC7159 only
                   )

                .. note::

                   Further branches could be added to json-objects,
                   and json-arrays only, while values in RFC7159 and RFC8259
                   mode permit replacement only. Objects support string indexes,
                   arrays integer indexes.

            kargs:
                For the complete set of call parameters refer to
                the method **JSONData.setkargs()**.

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

                **schema**:
                    A valid in-memory JSONschema.

                    default:= None

                **validator**:
                    Sets schema validator for the data file.
                    Curren release relies on *jsonschema*, which
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

            Results in an initialized object.

        Raises:

            NameError

            JSONDataValueError

            jsonschema.ValidationError

            jsonschema.SchemaError

        """
        # static final defaults

        self.schemafile = None

        # JSON-Syntax modes
        self.mode_json = MJ_RFC7159
        self.mode_schema = MS_DRAFT4
        self.mode_pointer = MJ_RFC6901
        self.mode_patch = MJ_RFC6902

        self.saveContext = True

        self.branch = None
        self.data = None
        self.schema = None
        self.indent = 4
        self.sort_keys = False
        self.validator = MS_OFF  # default validator

        self.jsonsyn = JSYN_NATIVE

        self.op_depth = 0
        self.op_ignore = []
        self.op_use = []
        self.state_pre = []

        self.op_cp_pol = kargs.get('copy', C_DEFAULT)

        if __debug__:
            self.debug = False
        self.verbose = False

        # fetch keyword parameters
        self.setkargs(**kargs)

        #
        # fetch JSON document
        #
        if type(jdata) in (list, dict, ):  # object or array
            if self.op_cp_pol == C_REF:
                self.data = jdata
            elif self.op_cp_pol == C_SHALLOW:
                self.data = copy.copy(jdata)
            elif self.op_cp_pol == C_DEEP:
                self.data = copy.deepcopy(jdata)

        elif isinstance(jdata, JSONData):  # copy constructor
            self.data = copy.deepcopy(jdata.data)
            self.schema = jdata.schema
            self.schemafile = jdata.schemafile
            self.mode_json = jdata.mode_json
            self.mode_schema = jdata.mode_schema
            self.mode_pointer = jdata.mode_pointer
            self.mode_patch = jdata.mode_patch
            self.saveContext = jdata.saveContext
            self.indent = jdata.indent
            self.sort_keys = jdata.sort_keys
            self.validator = jdata.validator
            self.op_depth = jdata.op_depth
            self.op_ignore = jdata.op_ignore[:]
            self.op_use = jdata.op_use[:]
            self.state_pre = jdata.state_pre[:]

            try:
                if self.op_cp_pol == C_REF:
                    self.data = jdata()
                elif self.op_cp_pol == C_SHALLOW:
                    self.data = copy.copy(jdata())
                elif self.op_cp_pol == C_DEEP:
                    self.data = copy.deepcopy(jdata())
            except:
                raise JSONDataError("Non-valid JSON data:" +
                                        str(jdata))

        else:  # values for RFC7159/RFC8259
            if self.mode_json == MJ_RFC4627:
                raise JSONDataError(
                    "Mode RFC4627 - Non-valid JSON data, requires object or array: %s - %s"
                    % (str(type(jdata)), str(jdata)))

            try:
                if self.op_cp_pol == C_REF:
                    self.data = jdata
                elif self.op_cp_pol == C_SHALLOW:
                    self.data = copy.copy(jdata)
                elif self.op_cp_pol == C_DEEP:
                    self.data = copy.deepcopy(jdata)

            except:
                raise JSONDataError(
                    "Non-valid JSON data:" + str(jdata))

        if __debug__:
            if self.debug > 2:
                sys.stderr.write("DBG:JSON=           " + str(
                    myjson.__name__) + " / " + str(myjson.__version__)
                    + "\nDBG:self.data=    #[" + str(self.data) + "]#"
                    + "\nDBG:self.schema=  #[" + str(self.schema) + "]#\n"
                )
        elif self.verbose:
            print("VERB:JSON=          " + str(myjson.__name__)
                  + " / " + str(myjson.__version__))

        # Validate.
        if not self.schema and self.validator != MS_OFF:
            raise JSONDataParameterError("value", "schema", str(self.schema))

        # INPUT-BRANCH: validate data
        if self.validator != MS_OFF:
            self.validate(self.data, self.schema, self.validator)

    def setkargs(self, **kargs):
        """Sets key arguments.

        Args:

            kargs:

                **copydata**:
                    Controls the assignment policy for JSON data.
                    The schema is copied by reference only, once
                    read. ::

                       copydata := (
                            C_REF       # by reference
                          | C_DEEP      # by copy.deepcopy()
                          | C_SHALLOW   # by copy.copy()
                       )

                **debug**:
                    Displays extended state data for developers.
                    Requires __debug__==True.

                **depth**:
                    Sets the default behavior for the operators.
                    Controls, whether the hook only or the complete
                    branch is processed in depth node-by-node. ::

                       0:  the hook of the branch
                       #n: the level of the branch as integer, the
                           remaining sub-branch is treated by it's hook
                       -1: the complete branch

                    default:= 0

                **indent_str**:
                    Defied the indentation of 'str'.

                    default:= 4

                **jsonsyntax**:
                    The display syntax for JSON data with
                    *__str__*. ::

                       jsonsyntax := (
                            JSYN_NATIVE | 'json'
                          | JSYN_PYTHON | 'python'
                       )

                       JSYN_NATIVE: Native standards syntax.
                       JSYN_PYTHON: Python in-memory syntax.

                **mode**:
                    The mode of JSON processing: ::

                       mode := (
                            MJ_RFC4627 | 'rfc4627'
                          | MJ_RFC7493 | 'rfc7493'  # currently not supported, mapped to RFC7159
                          | MJ_RFC7159 | 'rfc7159'
                          | MJ_RFC8259 | 'rfc8259'
                          | MJ_ECMA404 | 'ecma404'  # same as RFC8259
                       )

                    default := MJ_RFC7159

                **rtype**:
                    Sets the data type of the returned result. ::

                       rtype := (
                            data    # returns the data record only - self.data
                          | jdata   # returns an object of class JSONData
                          | obj     # returns an object of own class
                       )

                    default := obj

                **saveContext**:
                    Saves and restores the defined context
                    parameters when entering a context call.

                    default:= True

                **schema**:
                    A valid in-memory JSONschema.

                    default:= None

                **sortstr**:
                    Sort display of 'str()' by key. ::

                        sortstr := (True | False)

                    default := True

                **validator**:
                    Sets schema validator for the data file.
                    Curren release relies on *jsonschema*, which
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

                **verbose**:
                    Extends the amount of the display of
                    processing data.

        Returns:
            instance/None

        Raises:

            NameError:

            JSONDataValueError

            jsonschema.ValidationError:

            jsonschema.SchemaError:

        """
        if __debug__:
            self.debug = False
        else:
            self.debug = kargs.get('debug', 0)

        self.verbose = kargs.get('verbose', False)


        #
        #self.op_cp_pol = kargs.get('copydata', C_DEFAULT)
        self.op_cp_pol = kargs.get('copydata', self.op_cp_pol)
        try:
            self.op_cp_pol = copy2c[self.op_cp_pol]
        except JSONDataKeyError:
            raise JSONDataValueError('copydata', str(self.op_cp_pol))

        self.indent_str = kargs.get('indent_str', 0)  #: for __str__
        self.sort_keys = kargs.get('sortstr', True)  #: for __str__

        self.jsonsyntax = kargs.get('jsonsyntax', JSYN_NATIVE)  #: controls context parameter restoration
        if self.jsonsyntax not in (JSYN_NATIVE, 'json', JSYN_PYTHON, 'python'):
            raise JSONDataError("Unknown syntax variant: jsonsyntax=" + str(self.jsonsyntax))

        self.saveContext = kargs.get('saveContext', 0)  #: controls context parameter restoration
        self.schema = kargs.get('schema', None)  #: The internal object schema for the framework - a fixed set of files as final MS_DRAFT4.

        #
        validator = kargs.get('validator', self.validator)
        try:
            self.validator = validator2ms[validator]
        except JSONDataKeyError:
            raise JSONDataValueError('validator', str(validator))

        # INPUT-BRANCH: schema for validation
        if validator != MS_OFF:  # validation requested, requires schema
            if not self.schema:  # no schema data present
                raise JSONDataError("value", "schema", self.schema)

        #
        self.mode_json = kargs.get('mode', self.mode_json)
        try:
            self.mode_json = mode2mj[self.mode_json]
        except JSONDataKeyError:
            raise JSONDataParameterError("Unknown mode:" + str(self.mode_json))

        #
        _d = kargs.get('depth')
        if _d:
            if _d in ('default', -1):
                self.op_depth = 0
            elif _d.isnumeric():
                self.op_depth = int(_d)
            else:
                raise JSONDataValueError("Not supported", str(_d))

        if self.verbose:
            print("VERB:JSON=          " + str(myjson.__name__) + " / " + str(
                myjson.__version__))

        # Check data.
        if kargs.get('data') and self.data  is None:
            raise JSONDataParameterError("value", "data", str(self.data))

        # Validate.
        if not self.schema and self.validator != MS_OFF:
            raise JSONDataParameterError("value", "schema", str(self.schema))

        # INPUT-BRANCH: validate data
        if self.validator != MS_OFF:
            self.validate(self.data, self.schema, self.validator)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, k):
        """Deletes an item of *self.data*.

        Args:
            k:
                Key or index of *self.data*.
                If *None* the *self.data* is assigned *None*.

        Returns:
            None

        Raises:
            JSONDataKeyError

            IndexError

        """
        if isinstance(self.data, (dict, list)):
            del self.data[k]  # for now want the exeption
        raise JSONDataKeyError("requires object(dict) of array(list)")

    def get_data_items(self):
        """Returns a dictionary for objects as well as arrays.
        Arrays are returned as a *dict* with interger indexes as keys,
        while objects - *dict* - are returned by the native *items()*
        call.

        If required else use the attributes directly.

        """
        if type(self.data) is dict:
            return self.data.items()
        elif type(self.data) is list:
            ret = {}
            for i in range(len(self.data)):
                ret[i] = self.data[i]
            return ret.items()

    def get_data_keys(self):
        """Returns a list of keys for objects, or a list of indexes
        for arrays, thus enabling common access.

        Args:
            None

        Returns:
            For objects - dict - a list of keys,
            for arrays - list - a list of integer indexes.

        Raises:
            pass-through
        """
        if type(self.data) is dict:
            return self.data.keys()
        elif type(self.data) is list:
            ret = {}
            for i in range(len(self.data)):
                ret[i] = self.data[i]
            return ret.items()


    def __setitem__(self, k, v):
        """Assigns a value to an item of *self.data*.
        """
        if isinstance(self.data, (list, dict,)):
            self.data[k] = v
        else:
            raise JSONDataKeyError("requires object(dict) of array(list)")

    def __enter__(self):
        """Context for processing of specific parameter setups.

        Args:

            Context Parameters:
                See setargs. ::

                   copy, rtype, saveContext


        Returns:

        Raises:

        """
        if self.saveContext:
            self.state_pre.append([
                self.mode_json,
                self.mode_schema,
                self.mode_pointer,
                self.mode_patch,
                self.indent,
                self.sort_keys,
                self.validator,
                self.op_depth,
                self.op_ignore,
                self.op_use,
            ])
        return self.deepcopy()

    def __exit__(self, exc_type, exc_value, traceback):
        """Resets the context to the parameter setup before the last call of 'enter'.

        """
        if self.saveContext:
            (self.mode_json, self.mode_schema, self.mode_pointer,
             self.mode_patch, self.indent, self.sort_keys, self.validator,
             self.op_depth, self.op_ignore, self.op_use,
            ) = self.state_pre.pop()

    def __bool__(self):
        """The boolean value of the contained data status *JSONData*.

        Args:
            None

        Returns:
            True:  has any data
            False: no data contained, this is also the case for empty *list* and *dict*


        """
        return self.data not in (None, {}, [])

    def __nonzero__(self):
        """The boolean value of the contained data status *JSONData*.

        Args:
            None

        Returns:
            True:  has any data
            False: no data contained, this is also the case for empty *list* and *dict*


        """
        return self.data not in (None, {}, [])

    def __call__(self, *args, **kargs):
        """Evaluates the pointed value from the document.

        The operation::

           z = S(x)

        Returns the top node referenced by the JSON-Pointer 'x' in accordance to RFC6901::

           z = ( S => x )

        Args:
            *args:

                args[0]:
                    An optional valid JSONPointer.

                    default:='' => top, see [RFC6901]_

            **kargs:

                **copydata**:
                    Use of input parameters for processing. ::

                       copydata := (
                            C_DEEP     | 'deep'
                          | C_REF      | 'ref'
                          | C_SHALLOW  | 'shallow')

                    default := C_REF

        Returns:
            The pointed value, or None.

        Raises:
            JSONPointerError

        """
        if not args:
            x = ''
        else:
            x = args[0]
        c = kargs.get('copydata')
        if c:
            if c in ('deep', C_DEEP):
                if isinstance(x, JSONPointer):
                    return copy.deepcopy(x.get_node_value(self.data))
                return copy.deepcopy(
                    JSONPointer(x).get_node_value(self.data))
            elif c in ('shallow', C_SHALLOW):
                if isinstance(x, JSONPointer):
                    return copy.copy(x.get_node_value(self.data))
                return copy.copy(JSONPointer(x).get_node_value(self.data))
            elif c in ('ref', C_REF):
                pass
            else:
                raise JSONDataError("Unknown copy type:" + str(c))

        if isinstance(x, JSONPointer):
            return x.get_node_value(self.data)
        return JSONPointer(x).get_node_value(self.data)

    def __eq__(self, x):
        """Compares this JSONData.data with x.

        The operations: ::

           S == x

        Returns the result of comparison: ::

           z = ( S == x )

        Args:

            x: A valid JSONData.

        Context Parameters:

            See setargs.

        Returns:

            True or False

        Raises:

            JSONDataError
        """
        if not self.data and not x:  # all None is equal,...
            return True
        elif not self.data or not self.data:  # ...one only is not
            return False

        if type(x) in (dict, list, ):  # is a tree...
            return self.data == x
        elif isinstance(x, JSONData):  # is a container
            return self.data == x.data
        return self.data == x  # is any atom

    def __repr__(self):
        """Dump data.
        """
        return repr(self.data)

    def __str__(self):
        """Dumps data by pretty print.

        The data representation is controlled by the
        variable 'self.jsonsyn' ::

           JSONData.jsonscope := (JSYN_NATIVE | JSYN_PYTHON)

           JSYN_NATIVE: "Literally in accordance to standards."
           JSYN_PYTHON: "Python in-memory syntax representation."

        """
        if self.jsonsyn == JSYN_NATIVE:
            return myjson.dumps(
                self.data, indent=self.indent, sort_keys=self.sort_keys)
        elif self.jsonsyn == JSYN_PYTHON:
            s = myjson.dumps(
                self.data, indent=self.indent, sort_keys=self.sort_keys)
            s = re.sub("true", "True", s)
            s = re.sub("false", "False", s)
            s = re.sub("null", "None", s)
            return s
        else:
            raise JSONDataError("JSON syntax variant not supported." + str(self.jsonsyn))

    def __getitem__(self, sel):
        """Gets an  entry of *self.data*.

        Args:
            sel:
                Selector, either a key, or an index.

        Returns:
            The entry at the location,
            or raises en exception.

        Raises:
            JSONDataKeyError(KeyError)

            JSONDataIndexError(IndexError)

        """
        try:
            return self.data[sel]
        except KeyError:
            raise JSONDataKeyError("object requires member name as key, got: " + str(sel))
        except IndexError:
            raise JSONDataIndexError("array requires index, got: " + str(sel))

    def __iter__(self):
        """Provides an iterator for contained native data.
        """
        return iter(self.data)

    def __ne__(self, x):
        """Compares this JSONData with x.

        Args:
            x:
                Valid JSONData.

        Returns:
            True or False

        Raises:
            JSONDataError
        """
        return not self.__eq__(x)

    def branch_add(self, sourcenode, targetnode='', key=None, **kargs):
        """Add a complete branch into a target structure of type object.
        Present branches are replaced, non-existent branches are
        added.

        The parent of the insertion point has to exist by default,
        see [RFC6902]_. If the target is an array, the source is either
        appended, or inserted [RFC6902]_.

        Args:
            **sourcenode**:
                Source branch to be inserted into the target tree.
                Either from within self-data, or an external source: ::

                  sourcenode := <commonnode>       # see class header

            **targetnode**:
                Target node within self-data, where the branch is to be inserted. ::

                  targetnode := <innode>           # see class header

                default := ''                      # the top of the 'whole document'

            **key**:
                Hook for the insertion within the target node. If not
                provided the contents of the target node itself are
                replaced by the source node.

                default := None

            kargs:
                **copydata**:
                    The type of creation of the added branch. ::

                        copydata := (
                              C_REF        # copy the reference only
                            | C_DEEP       # call copy.deepcopy()
                            | C_SHALLOW    # call copy.copy()
                        )

                    default := C_DEEP

        Returns:
            When successful returns *True*, else returns
            either *False*, or raises an exception.

        Raises:
            JSONDataNodeError:
                The target node is not contained in current object.

            JSONDataNodeTypeError:
                The types mismatch.

            JSONDataKeyError:
                Key mismatch.

        """
        ret = False
        _copy = kargs.get('copydata', C_DEEP)

        def _cp(v):
            if _copy == C_DEEP:
                return copy.deepcopy(v)
            elif _copy == C_SHALLOW:
                return copy.copy(v)
            if _copy == C_REF:
                return v
            else:  # default
                return copy.deepcopy(v)

        if isinstance(sourcenode, JSONPointer):
            sourcenode = sourcenode(self.data, False)
        elif type(sourcenode) in ISSTR:
            try:
                sourcenode = JSONPointer(sourcenode)
            except JSONPointerTypeError:
                # when not a pointer, than is assumed to be a value
                if sourcenode[0] == '/':
                    # it was a valid absolute pointer, so it is actually an error
                    raise

        elif isinstance(sourcenode, JSONData):
            sourcenode = sourcenode.data


        if targetnode is "":
            targetnode = self.data
        elif type(targetnode) in ISSTR:
            targetnode = JSONPointer(targetnode)
        elif isinstance(targetnode, JSONData):
            targetnode = targetnode.data

        if isinstance(targetnode, JSONPointer):
            try:
                if not key:
                    targetnode, key = targetnode.get_node_and_key(self.data)
                else:
                    targetnode = targetnode(self.data, False)
            except JSONDataKeyError:
                raise
            except Exception as e:
                # requires some more of a new path than for the node-only
                if key:
                    if type(key) == int:
                        self.branch_create('', targetnode, [])
                    else:
                        self.branch_create('', targetnode, {})
                if not key:
                    targetnode, key = targetnode.get_node_and_child(self.data)
                else:
                    targetnode = targetnode(self.data)

        if type(targetnode) == dict:
            if key:
                targetnode[key] = _cp(sourcenode)
            else:
                if type(sourcenode) != dict:
                    raise JSONDataNodeTypeError(
                        "type", "dict-target requires a key:targetnode/sourcenode",
                        str(type(targetnode)) + "/" + str(type(sourcenode)))
                for k, v in sourcenode.items():
                    targetnode[k] = _cp(v)

            return True

        elif type(targetnode) == list:
            if key  is None:

                # source list items extend contents of the target list
                if type(sourcenode) is list:
                    targetnode.extend(_cp(sourcenode))

                # source dictionaries replace the list
                elif type(sourcenode) is dict:
                    targetnode.append(sourcenode)

            elif key == '-' or key == len(targetnode):
                targetnode.append(_cp(sourcenode))
                ret = True

            elif 0 <= key < len(targetnode):
                targetnode.insert(key, _cp(sourcenode))

            else:
                raise JSONDataKeyError(
                    "mismatch:node:type", 'key', key, 'key-type',
                    type(key), 'node-type', type(targetnode))

            return True

        else:
            raise JSONDataNodeTypeError(
                "type", "requires array or object for targetnode: targetnode/sourcenode",
                str(type(targetnode)) + "/" + str(type(sourcenode)))

        return ret

    def branch_copy(self, sourcenode, targetnode='/', key=None, force=True):
        """Copies the source branch to the target node.
        The *branch_copy* is internally mapped to the call *branch_add*,
        thus shares basically the same parameters and behavior.

        Args:

            **sourcenode**:
                Source branch to be copied into target tree.
                Either from within self-data, or an external source: ::

                  sourcenode := <commonnode>       # see class header

            **targetnode**:
                Target node for the branch. Either from within self-data,
                or an external source: ::

                  targetnode := <innode>           # see class header

                default := '/'

            **key**:
                Optional key for the insertion point within target
                node, if not provided the target node itself.

            **force**:
                If true present are replaced, else only non-present
                targets are copied.

                default := True

        Returns:
            When successful returns *True*, else returns either *False*,
            or raises an exception.

        Raises:
            JSONDataError

            pass-through
        """
        if force:  # force replace of existing
            return self.branch_add(sourcenode, targetnode, key)

        elif type(targetnode) == list:
            if key == '-':
                pass
            elif not key  is None:
                if 0 <= key < len(targetnode):
                    if targetnode[key]:
                        raise JSONDataError("Node exists.")
                if len(targetnode) > len(sourcenode):
                    raise JSONDataError("Node exists.")
            else:
                if type(sourcenode) is list:
                    if targetnode:
                        raise JSONDataError("Node exists.")

        elif type(targetnode) == dict:
            if key:
                if targetnode.get(key, None):
                    raise JSONDataError("Node exists.")
            else:
                if type(sourcenode) is dict:
                    if targetnode:
                        raise JSONDataError("Node exists.")

        return self.branch_add(sourcenode, targetnode, key)

    def branch_create(self, branchpath, targetnode=None, padding_value=None):
        """Creates an abitrary relative branch from a path description
        located at *targetnode*. Intermediate nodes are created automatically
        when missing.

        The requested branch is created as the relative child branch
        of the provided *targetnode*. The *targetnode* must exist,
        while the child node - *branchpath[0]* - must not.

        Args:

            **branchpath**:
                New branch to be created in the target node.
                A Pointer address path relative to the *targetnode*. ::

                  branchpath := <commonnode>           # see class header

            **targetnode**:
                Base node for the created branch, must exist
                and located within the data tree of current object. ::

                  targetnode := <innode>           # see class header

                default := "/"

            **padding_value**:
                Optional default value, either an atomic type or a sub-branch
                itself. This value is only used for a new leaf, in case of
                an existent node the value is ignored.

                default := "null" / *None*

        Returns:
            When successful returns the created node, else returns
            either *None*, or raises an exception.

        Raises:
            JSONDataError

            JSONDataKeyError

            JSONDataNodeTypeError

            JSONDataParameterError

            JSONDataPathError
        """
        ret = None

        def get_newnode_of_type(bkeytype):
            """Fetch the required type for the new container."""
            if not bkeytype:
                return None

            if len(bkeytype) < 2:
                if bkeytype[0] == '-':  # RFC6902
                    return []
                elif type(bkeytype[0]) is int:  # array
                    return []
                elif type(bkeytype[0]) in (
                        str,
                        unicode, ):  # object
                    return {}
            else:
                if bkeytype[1] == '-':  # RFC6902
                    return []
                elif type(bkeytype[1]) is int:  # array
                    return []
                elif type(bkeytype[1]) in (
                        str,
                        unicode, ):  # object
                    return {}

            raise JSONDataKeyError("type", 'keytype', str(bkeytype))

        #
        # prepare branchpath
        if type(branchpath) in ISSTR:
            branchpath = JSONPointer(branchpath)

        if not isinstance(branchpath, list):  # basic behaviour rfc6902
            raise JSONDataPathError("type", "branchpath", branchpath)

        #
        # prepare target node
        if targetnode is None:
            tnode = self.data

        elif isinstance(targetnode, JSONPointer):
            try:
                tnode = targetnode(self.data)

            except TypeError:
                raise JSONDataNodeTypeError(
                    "Requires container, got type='%s' in target node:'%s'" %
                    (str(type(tnode)), str(targetnode.get_raw()) ))

            except (KeyError, JSONPointerError):
                raise JSONDataKeyError(
                    "Requires present node, missing target node:'%s'" %
                    (str(targetnode.get_raw()) ))

        elif targetnode == '':  # RFC6901 - whole document
            tnode = self.data

        else:
            tnode = targetnode

        if type(tnode) == dict:
            # target is an object

            # Be aware, the special '-' could be a valid key, thus cannot be prohibited!!!
            if type(branchpath[0]) not in ISSTR:
                raise JSONDataPathError(
                    "type", "branchpath",
                    str(type(tnode)) + "/" +str(branchpath))

            if len(branchpath) > 1:
                # actual branch items
                if not tnode.get(unicode(branchpath[0]), False):
                    tnode[unicode(branchpath[0])] = get_newnode_of_type(branchpath)

                ret = self.branch_create(
                    branchpath[1:], tnode[branchpath[0]], padding_value)

            else:
                # the leaf item - putting this onto an existing will
                # remove the previous value
                if not tnode.get(branchpath[0], False):
                    ret = tnode[unicode(branchpath[0])] = self.get_canonical_value(padding_value)
                else:
                    ret = tnode[unicode(branchpath[0])]

        elif type(tnode) == list:
            # target is an array

            # see RFC6902 for '-'/append
            if type(branchpath[0]) in (int, ) and branchpath[0] <= len(tnode):
                pass
            elif unicode(branchpath[0]) == u'-':  # see RFC6902 for '-'/append
                pass
            else:
                raise JSONDataNodeTypeError(
                    "index-value", "targetnode/branch:" + str(type(tnode))
                    + " list-index requires int(i <= len()) or '-', got "
                    + str(type(branchpath[0])) + " '" + str(branchpath) + "'"
                    )

            if len(branchpath) == 1:
                if branchpath[0] == '-':
                    branchpath[0] = len(tnode)
                    tnode.append(self.get_canonical_value(padding_value))
                else:
                    tnode[branchpath[0]] = self.get_canonical_value(padding_value)
                ret = tnode
            else:
                if branchpath[0] == '-':
                    tnode.append(get_newnode_of_type(branchpath))
                    ret = self.branch_create(
                        branchpath[1:], tnode[-1], padding_value)
                elif tnode != None and branchpath[0] == len(tnode):
                    tnode.append(get_newnode_of_type(branchpath))
                    ret = self.branch_create(
                        branchpath[1:], tnode[-1], padding_value)

        else:
            raise JSONDataNodeTypeError(
                "type", "existing targetnode", str(targetnode) + " = "+ str(type(tnode)) + " requires: list or dict")

        return ret

    def branch_move(self,
                    sourcenode,
                    targetnode=None,
                    key=None,
                    force=False):

        """Moves a branch to the target node.

        Args:

            **sourcenode**:
                Source branch to be moved into the target node.
                Must be member of the self-data structure, else use
                either *branch_add* or *branch_copy*.
                Either from within self-data, or an external source: ::

                  sourcenode := <innode>       # see class header

            **targetnode**:
                Target node for the branch. ::

                  targetnode := <innode>       # see class header

                default := '/'

            **key**:
                Optional key for the insertion point within target
                node, if not provided the target node itself.

            **force**:
                If true present are replaced, else only non-present
                are copied.

                default := True

        Returns:
            When successful returns *True*, else returns either
            *None*, or raises an exception.

        Raises:
            JSONDataError

            JSONDataKeyError
        """
        ret = self.branch_copy(sourcenode, targetnode, key, force)
        if ret:
            ret1 = self.branch_remove(sourcenode)
            return ret & ret1
        return ret

    def branch_remove(self, targetnode, key=None, rfc6902=True):
        """Removes a branch from a contained data in self.

        Args:

            **targetnode**:
                Container with item to be removed. ::

                  targetnode := <innode>       # see class header

            **key**:
                Key of insertion point within target node, if not
                provided the target node itself.

            **rfc6902**:
                If *True* the removed element has to be present,
                else non-present is simply ignored.

        Returns:
            When successful returns *True*, else returns
            either *False*, or raises an exception.

        Raises:
            JSONDataKeyError

            JSONDataNodeTypeError
        """
        if type(targetnode) in ISSTR:
            _targetnode = JSONPointer(targetnode)

        elif type(targetnode) is list:
            _targetnode = JSONPointer(targetnode)

        elif isinstance(targetnode, JSONPointer):
            _targetnode = targetnode

        else:
            raise JSONDataNodeTypeError("Requires path within self:got:" + str(type(targetnode)))

        try:
            if not key:
                _targetnode = targetnode(self.data, True)
                key = targetnode[-1]
            else:
                _targetnode = targetnode(self.data, False)

        except (KeyError, TypeError, IndexError):
            raise JSONDataKeyError("Key not found:" + str(key))

        except JSONPointerError:
            if rfc6902:
                raise JSONDataKeyError("Requires present node" + str(targetnode) + str(key))
            return True

        try:
            _targetnode.pop(key)
            return True
        except (IndexError, TypeError, KeyError):
            if rfc6902:
                raise JSONDataKeyError("Missing node within self: " + str(targetnode))
            return True

    def branch_replace(self, sourcenode, targetnode, key=None, rfc6902=True):
        """Replaces the value of the target node by the copy
        of the source branch.

        Requires in order to RFC6902, all items to be replaced
        has to be present. Thus fails by default if at least one
        is missing.

        Internally the 'branch_add()' call is used with a deep copy.
        When a swallow copy is required the 'branch_move()' has to be used.

        Args:
            **sourcenode**:
                Source branch to be inserted into target tree.
                Either from within self-data, or an external source: ::

                  sourcenode := <commonnode>   # see class header

            **targetnode**:
                Target where the branch is inserted. ::

                  targetnode := <innode>       # see class header

            **key**:
                Key of insertion point within target node, if not
                provided the target node itself.

            **rfc6902**:
                If *True* the removed element has to be present,
                else non-present is simply ignored.

        Returns:
            When successful returns *True*, else returns
            either *False*, or raises an exception.

        Raises:
            JSONDataError
        """
        if isinstance(targetnode, JSONPointer):
            try:
                if not key:
                    tnode, key = targetnode.get_node_and_key(self.data)
                else:
                    tnode = targetnode(self.data, False)

            except TypeError:
                raise JSONDataNodeTypeError(
                    "Requires container, got type='%s' in target node:'%s'" %
                    (str(type(tnode)), str(targetnode.get_raw()) ))

            except (KeyError, JSONPointerError):
                if rfc6902:
                    raise JSONDataKeyError(
                        "Requires present node, missing key='%s' in target node:'%s'" %
                        (str(key), str(targetnode.get_raw()) ))

        elif type(targetnode) in (list,):
            try:
                if not key:
                    tnode, key = JSONPointer(targetnode).get_node_and_key(self.data)
                else:
                    tnode = JSONPointer(targetnode)(self.data, False)

            except (KeyError, JSONPointerError):
                if rfc6902:
                    if len(str(targetnode)) > 30:
                        targetnode = str(targetnode)[:30] + '...'
                    raise JSONDataKeyError(
                        "Requires present node, missing key='%s' in target node:'%s'" %
                        (str(key), str(targetnode) ))
        else:
            if len(str(targetnode)) > 30:
                targetnode = str(targetnode)[:30] + '...'
            raise JSONDataNodeTypeError(
                "Requires parent container-node, got target node:'%s: %s'" %
                (str(type(targetnode)), str(targetnode)))

        return self.branch_add(sourcenode, tnode, key)

    def branch_superpose(self, sourcenode, targetnode=None, key=None, **kargs):
        """Superposes a branch recursively on to the current data tree 
        *self.data* with defined constraints. Provides partial mapping 
        in dependence of parameters and data entries of source and/or 
        target.

        The processing is controlled by logic operations on node 
        structures, which maps a logical tree of JSON nodes from the
        source node onto the subtree of JSON nodes defined by the target
        target node. The provided logic operators are related to structure,
        though the types of nodes, not the contents.
        
        For the provided logic operators refer to parameter *map*.

        Args:

            **sourcenode**:
                Value struct to be inserted.

                default := None

            **targetnode**:
                Data node within current document to be superposed.

                default := None  # whole document *self.data*

            **key**:
                Hook selector within the data tree spanned by the targetnode .

                default := None  # top of the targetnode

            kargs:
                **copy**:
                    Create a copy of the sourcenode. ::

                       copy := (
                            C_DEEP      # insert from copy.deepcopy() 
                          | C_SHALLOW   # insert from copy.copy()
                          | C_REF       # insert from the provided parameter
                          )

                    default := C_REF  # no copy, work on input

                **depth**: 
                    Sets the default behavior for the operators
                    on the data branches. Controls, whether the hook
                    only or the complete branch is processed in 
                    depth node-by-node. ::

                      0:  the hook of the branch
                      #n: the level of the branch as integer, the 
                          remaining sub-branch is treated by it's hook
                      -1: the complete branch

                    default:= 0

                **ignore**:
                    Ignores attributes including subtrees contained 
                    in the list. ::

                       ignore := [<list-of-rfc6901-path-items>]

                **map**:
                    Sets the default behavior for the mapping of
                    branches by operators. This is also influenced 
                    by the parameter 'op_depth'. ::

                      B_AND:  replace corresponding leafs only when any target node is present
                      B_OR:   replace corresponding items of source leafs
                      B_XOR:  insert only when no target node is present

                    default:= B_OR

                **use**:
                    Considers the listed attributes only as white list. ::

                       use := [<list-of-rfc6901-path-items>]

        Returns:
            *True* for success, else *False* or raises exception.

        Raises:
            JSONDataError

            JSONDataIndexError
            
            pass-through

        """
        # defaults
        _cp = C_REF
        _ign = self.op_ignore
        _use = self.op_use
        _dep = self.op_depth

        _mp = B_OR

        def _map(d0, s0, v0, n=0):
            """The core algorithm for the mapping of branches of Python
            structures by constraints. Includes resulting logic operations
            from constraints.
        
            The code tends to be monolithic, but saves memory and performance.
        
            Args:
                d0:
                    Data root.
        
                s0:
                    Key or index for hook.
        
                v0:
                    Value/branch to be hooked.
        
            Environment:
                Uses inherited variables from parent
                name spaces.
        
            Returns:
        
            Raises:
        
            """
            if self.op_ignore and s0 in self.op_ignore:  # blacklist
                return
            if self.op_use and s0 not in self.op_use:  # white list
                return
            if self.op_depth > 0 and n >= self.op_depth:  # depth
                return
            n += 1
            
            if s0 != None:
                try:
                    dx = d0
                    d0 = d0[s0]
                except TypeError:
                    if s0 == '-':
                        d0.append(v0)
                        return True
                    raise
                except KeyError:
                    d0[s0] = v0
                    return True
                except IndexError:
                    if len(d0) == s0:
                        d0.append(v0)
                        return True
                    raise JSONDataIndexError("out of range(>%s): %s" % (str(len(d0)), str(s0)))

            else:
                dx = d0

            if _mp in (B_OR,):  # add all items
                if type(d0) is dict:
                    if type(v0) is dict:
                        for k, v in v0.items():
                            _map(d0, k, v, n + 1)
                    elif s0 != None:
                        dx[s0] = v0
                    else:
                        dx = v0

                elif type(d0) is list:
                    if type(v0) is list:
                        for k in range(len(v0)):
                            _map(d0, k, v0[k], n + 1)
                    else:
                        if type(s0) is int:
                            if s0 < len(dx):
                                dx[s0] = v0
                            elif s0 == len(dx):
                                dx.append(v0)
                            else:
                                raise JSONDataIndexError("out of range(>%s): %s" % (str(len(dx)), str(s0)))
                        elif type(s0) in ISSTR:
                            dx[s0] = v0
                        return True
    
                else:
                    dx[s0] = v0

            elif _mp in (B_XOR, ):  # add non-present items
                if type(d0) is dict:
                    if not d0.get(s0):
                        if type(v0) is dict:
                            for k, v in v0.items():
                                _map(d0, k, v, n + 1)
                        elif s0 == '':
                            pass
                        else:
                            d0[s0] = v0

                elif type(d0) is list:
                    if type(v0) is list:
                        for k in range(len(v0)):
                            _map(d0, k, v0[k], n + 1)

                    else:
                        if type(dx) is dict:
                            if dx.get(s0):
                                dx[s0] = v0
                        elif type(dx) is list:
                            if len(dx) <= s0:
                                dx.append(v0)
                        else:
                            # cannot return a result assigned to a non-container
                            raise JSONDataError("internal error")
                        return True

                else:
                    if type(dx) is dict:
                        if not dx.get(s0):
                            dx[s0] = v0
                    elif type(dx) is list:
                        if len(dx) == s0:
                            dx.append(v0)
                    else:
                        # cannot return a result assigned to a non-container
                        raise JSONDataError("internal error")

            elif _mp in (B_AND, ):  # add present items
                if type(d0) is dict:
                    if not d0.get(s0):
                        for k, v in v0.items():
                            if d0.get(k):
                                _map(d0, k, v, n + 1)

                elif type(d0) is list:

                    if type(v0) is list:
                        for k in range(len(v0)):
                            if k < len(d0):
                                _map(d0, k, v0[k], n + 1)
                    else:
                        if type(dx) is dict:
                            if dx.get(s0):
                                dx[s0] = v0
                        elif type(dx) is list:
                            if len(dx) <= s0:
                                dx.append(v0)
                        else:
                            # cannot return a result assigned to a non-container
                            raise JSONDataError("internal error")
                        return True

                else:
                    dx[s0] = v0

            else:
                return False
            return True


        for k, v in kargs.items():
            if k == 'copy':
                if v in (
                        'deep',
                        C_DEEP, ):
                    _cp = C_DEEP

                elif v in (
                        'shallow',
                        C_SHALLOW, ):
                    _cp = C_SHALLOW

                elif v in (
                        'ref',
                        C_REF, ):
                    _cp = C_REF

                else:
                    raise JSONDataError("Unknown copy-type:" + str(v))

            elif k == 'ignore':
                _ign = v

            elif k == 'use':
                _use = v

            elif k == 'depth':
                _dep = v

            elif k == 'map':

                if v in (
                        B_AND,
                        B_OR,
                        B_XOR,
                        ):
                    _mp = v

                else:
                    raise JSONDataError("Unknown map:" + str(v))

        if targetnode is None:
            # use default
            targetnode = self.data

        elif type(targetnode) is list and (
            (key and type(key) not in (int, float,))
            and key != '-'  # see RFC6901
            ):
            # incompatible index type
            raise JSONDataError("list index mismatch" + str(key))

        elif type(targetnode) is dict:
            # almost anything permitted
            pass

        elif isinstance(targetnode, JSONPointer):
            # pointer object, tranfrom to a node
            targetnode = targetnode(self.data)

        elif type(targetnode) in ISSTR:
            # assume a pointer string, tranfrom to a node
            targetnode = JSONPointer(targetnode)(self.data)

        #
        # special: document root-changes by non-container for RFC7159
        #
        if key == None and (
                type(sourcenode) not in (dict, list)
                or type(sourcenode) != type(targetnode)
            ):
            if not self.mode_json & MJ_RFC7159 and type(sourcenode) not in (dict, list):
                raise JSONDataError("basic document types require mode RFC7159: " + str(sourcenode))
                
            if _mp in (
                    B_OR,
                ):
                self.data = sourcenode
            elif _mp in (
                    B_AND,
                ) and (
                    (self.data and sourcenode)
                    or (self.data == None and sourcenode == None)
                    or (self.data != None and sourcenode != None)
                ):
                self.data = sourcenode
            elif _mp in (
                    B_XOR,
                ) and not (
                    (self.data and sourcenode)
                    or (self.data == None and sourcenode == None)
                    or (self.data != None and sourcenode != None)
                ):
                self.data = sourcenode

            return True

        if _cp is C_DEEP:
            _dat = copy.deepcopy(targetnode)

        elif _cp is C_REF:
            _dat = targetnode

        elif _cp is C_SHALLOW:
            _dat = copy.copy(targetnode)

        if _mp in (
                B_OR,
                B_XOR,
                B_AND, ):
            _map(_dat, key, sourcenode, n=0)

        return True

    def branch_test(self, targetnode, value):
        """Tests match in accordance to RFC6902.

        Args:
            **targetnode**:
                Node to be compared with the value. Due to
                ambiguity the automated conversion is not
                reliable, thus it has to be valid. ::

                  targetnode := <innode>       # see class header

            **value**:
                Expected value for the given node.

        Returns:
            When successful returns 'True', else returns 'False'.

        Raises:
            JSONDataError
        """
        if not targetnode and not value:  # all None is equal,
            return True
        elif type(targetnode) in ISSTR:
            return JSONPointer(targetnode).get_node_value(self.data) == value
        elif isinstance(targetnode, JSONPointer):
            return targetnode.get_node_value(self.data) == value

    def get_data(self):
        """Returns the reference to data."""
        return self.data

    def get_schema(self):
        """Returns the reference to schema."""
        return self.schema

    def clear(self):
        """Clears the contained data.
        """
        if isinstance(self.data, dict):
            self.data.clear()
        elif isinstance(self.data, list):
            [x.pop() for x in reversed(self.data)]
        else:
            self.data = None
        return True

    def copy(self):
        """Creates a shallow copy of self.
        """
        return JSONData(self.data, copydata=C_SHALLOW)

    def deepcopy(self):
        """Creates a deep copy of self, including referenced data.
        The schema is kept as a shared reference.
        """
        return JSONData(self.data, copydata=C_DEEP)

    def get(self, key, default=None):
        """Transparently passes the 'get()' call to 'self.data'."""
        return self.data.get(key, default)

    def get_canonical_value(self, node):
        """Fetches a copy of the canonical value represented by
        the node. The actual value could be either an atomic value,
        a node representing a branch, or a reference to
        an atomic value.
        Creates a deep copy, thus references are no longer
        valid.

        Args:
            **value**:
                Value pointer to be evaluated to the actual
                value. Valid input types are:

                    int,str,unicode:
                        Integer, kept as an atomic integer
                        value.

                    dict,list:
                        Assumed to be a valid node for 'json'
                        package, used by reference.

                    JSONPointer:
                        A JSON pointer in accordance to
                        RFC6901.

        Returns:
            When successful returns the value, else returns
            either 'False', or raises an exception.

        Raises:
            JSONDataError

        """
        if type(node) in (dict, list):  # assumes a 'json' package type node
            return node
        elif type(node) in (
                int,
                float, ):  # assume a 'JSON' RFC7159 int, float
            return node
        elif type(node) in (
                str,
                unicode, ):  # assume a 'JSON' RFC7159 string
            return unicode(node)
        elif isinstance(node, JSONPointer):  # assume the pointed value
            return node.get_node_value(self.data, C_DEEP)
        elif not node:
            return None
        else:
            raise JSONDataError("type", "value", str(node))

    def pop(self, key):
        """Transparently passes the 'pop()' call to 'self.data'."""
        return self.data.pop(key)

    def dump_data(self, pretty=PJ_TREE, **kargs):
        """Prints structured data.

        Args:

            **pretty**:
                Activates pretty printer, else flat. ::

                   format := (
                        PJ_TREE    # tree view JSON syntax
                      | PJ_FLAT    # flat print JSON syntax
                      | PJ_PYTREE  # tree view Python syntax
                      | PJ_PYFLAT  # flat print Python syntax
                      | PJ_REPR    # repr() - raw string, Python syntax
                      | PJ_STR     # str() - formatted string, Python syntax
                   )

            kargs:
                **source**:
                    Prints data within 'source'.

                    default:=self.data

        Returns:
            When successful returns 'True', else returns either
            'False', or raises an exception.

        Raises:
            pass-through
        """
        source = kargs.get('source', source = self.data)

        if pretty == PJ_TREE:
            print(myjson.dumps(source, indent=self.indent))
        elif pretty == PJ_FLAT:
            print(myjson.dumps(source))
        elif pretty == PJ_PYTREE:
            print(myjson.dumps(source, indent=self.indent))
        elif pretty == PJ_PYFLAT:
            print(str(source))
        elif pretty == PJ_REPR:
            print(repr(source))
        elif pretty == PJ_STR:
            print(str(source))
        else:
            print(myjson.dumps(source, indent=self.indent))


    def dump_schema(self, pretty=True, **kargs):
        """Prints structured schema.

        Args:

            **pretty**:
                Activates pretty printer for treeview,
                else flat.

            kargs:
                **source**:
                    Prints schema within 'source'.

                    default:=self.schema

        Returns:
            When successful returns 'True', else returns
            either 'False', or raises an exception.

        Raises:
            pass-through

        """
        source = kargs.get('source', self.schema)

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def set_schema(self, schemafile=None, targetnode=None, **kargs):
        """Sets schema or inserts a new branch into the current
        assigned schema.

        The main schema(targetnode==None) is the schema related
        to the current instance. Additional branches could be added
        by importing the specific schema definitions into the main
        schema. These could either kept volatile as a temporary
        runtime extension, or stored into a new schema file in order
        as extension of the original for later combined reuse.

        Args:
            **schemafile**:
                JSON-Schema filename for validation of the
                subtree/branch. See also **kargs['schema'].

            **targetnode**:
                Target container hook for the inclusion of
                the loaded branch.

            kargs:
                **schema**:
                    In-memory JSON-Schema as an alternative
                    to schemafile. When provided the 'schemafile'
                    is ignored.

                    default:=None

                **validator**:
                    Sets schema validator for the data file.
                    The values are: ::

                       validator := (
                            default = validate,
                          | draft3  = Draft3Validator,
                          | off     = None.
                       )

                    default:= validate

                **persistent**:
                    Stores the 'schema' persistently into 'schemafile'
                    after completion of update including addition of
                    branches. Requires valid 'schemafile'.

                    default:=False

        Returns:
            When successful returns 'True', else returns either
            'False', or raises an exception.

        Raises:

            JSONDataError

            JSONDataSourceFileError

            JSONDataValueError

        """
        if __debug__:
            if self.debug:
                print("DBG:set_schema:schemafile=" + str(schemafile))

        #
        #*** Fetch parameters
        #
        persistent = False
        schema = None
        for k, v in kargs.items():
            if k == 'validator':  # controls validation by JSONschema
                if v == 'default' or v == MS_DRAFT4:
                    self.validator = MS_DRAFT4
                elif v == 'draft3' or v == MS_DRAFT3:
                    self.validator = MS_DRAFT3
                elif v == 'off' or v == MS_OFF:
                    self.validator = MS_OFF
                else:
                    raise JSONDataValueError("unknown", k, str(v))
            elif k == 'schema':
                schema = v
            elif k == 'persistent':
                persistent = v

        if schemafile != None:  # change filename
            self.schemafile = schemafile
        elif self.schemafile != None:  # use present
            schemafile = self.schemafile

        if not schemafile:
            if persistent:  # persistence requires storage
                raise JSONDataTargetFileError("open", "JSONSchemaFilename",
                                         schemafile)

        # schema for validation
        if schema:  # use loaded
            pass

        elif schemafile:  # load from file
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

            self.branch_add(targetnode, None, schema)

        return schema != None

    def validate(self, data, schema, validator=None):
        """Validate data with schema by selected validator.

        Args:

            **data**:
                JSON-Data.

            **schema**:
                JSON-Schema for validation.

            **validator**:
                Validator to be applied, current supported:

                    schema:

                        In-memory JSON-Schema as an alternative
                        to schemafile. When provided the 'schemafile'
                        is ignored.

                        default:=None

                **validator**: [default, draft3, draft4, off, on, ]
                    Sets schema validator for the data file.

                        default|MS_ON:
                            The current default.

                        draft3|MS_DRAFT3:
                            The first supported JSONSchema IETF-Draft.

                        draft4|MS_DRAFT4:
                            The current supported JSONSchema IETF-Draft.

                        off|MS_OFF:
                            No validation.

                    default:= MS_DRAFT4

        Returns:
            When successful returns 'True', else returns
            either 'False', or raises an exception.

        Raises:

            JSONDataValidationError

            JSONDataSchemaError

            JSONDataValueError
        """
        if not validator:
            validator = self.mode_schema

        if validator == MS_DRAFT4:
            if self.verbose:
                print("VERB:Validate: draft4")
            try:
                jsonschema.validate(data, schema)

            except JSONDataValidationError as e:
                print("ValidationError"
                      + "\n" + str(e)
                      + "\n#---"
                      + "\n" + str(dir(e))
                      + "\n#---"
                      + "\n" + str(e)
                      + "\n#---"
                      + "\n" + repr(e)
                      + "\n#---"
                      )
                raise

            except JSONDataSchemaError as e:
                print("SchemaError"
                      + "\n" + str(e)
                      + "\n#---"
                      + "\n" + str(dir(e))
                      + "\n#---"
                      + "\n" + str(e)
                      + "\n#---"
                      + "\n" + repr(e)
                      + "\n#---"
                      + "\n" + "path:" + str(e.path)
                      + "\n" + "schema_path:" + str(e.schema_path)
                      + "\n#---"
                      )
                raise

        elif validator == MS_DRAFT3:
            if self.verbose:
                print("VERB:Validate: draft3")
            jsonschema.Draft3Validator(data, schema)

        elif validator != MS_OFF:
            raise JSONDataValueError("unknown", "validator", str(validator))


from jsondata.jsonpointer import JSONPointer
# avoid nested recursion problems
