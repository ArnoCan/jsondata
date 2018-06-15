"""Modular processing of JSON data by trees and branches, pointers and patches.
"""

import sys
import os

import filesysobjects.userdata
import filesysobjects.osdata

__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.21'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'


#
# used for default names
appname = 'jsondata'

class JSONDataError(Exception):
    """ base Exception."""

    def __init__(self, *arg):
        """To be replaced by derived Exceptions.

        Fetch standard parameters and forward message to base class 'Exception'.
        """
        self.fetch(*arg)
        Exception.__init__(self, self.s)

    def fetch(self, *arg):
        """Fetch arguments.

        Args:
            *args:
                The following order is expected:

                0. Reason of exception.

                1. Name of object that caused the exception.

                2. Value of the object.

        Returns:
            None.

        Raises:
            None.
        """
        self.s = ""
        for a in arg:
            self.s += ":" + str(a)
        self.s = self.s[1:]

    def __repr__(self):
        """Cause: <reason>:<object>:<value>"""
        return self.s

    def __str__(self):
        """Cause with additional header text."""
        return "ERROR::" + self.s

# Sets display for inetractive JSON/JSONschema design.
_interactive = False


V3K = False  #: Python3.5+
if sys.version_info[:2] > (3, 4,):
    V3K = True
    ISSTR = (str,)
    """string and unicode"""

elif sys.version_info[:2] > (2, 6,) and sys.version_info[:2][0] < 3:
    ISSTR = (str, unicode,)  # @UndefinedVariable
    """string and unicode"""

else:
    raise JSONDataError(
        "Requires Python 2.7+, or 3.5+:" +
        str(sys.version_info[:2]))

#
# generic exceptions
#


class JSONDataIndexError(JSONDataError, IndexError):
    """ Error on key."""

    def __init__(self, *arg):
        JSONDataError.__init__(self, *arg)
        JSONDataError.fetch(self, *arg)
        IndexError.__init__(self, self.s)

    def __str__(self):
        return "JSONDataIndexError:" + self.s


class JSONDataKeyError(JSONDataError, KeyError):
    """ Error on key."""

    def __init__(self, *arg):
        JSONDataError.__init__(self, *arg)
        JSONDataError.fetch(self, *arg)
        KeyError.__init__(self, self.s)

    def __str__(self):
        return "JSONDataKeyError:" + self.s


class JSONDataPathError(JSONDataError, KeyError):
    """ Error on key."""

    def __init__(self, *arg):
        JSONDataError.__init__(self, *arg)
        JSONDataError.fetch(self, *arg)
        KeyError.__init__(self, self.s)

    def __str__(self):
        return "JSONDataPathError:" + self.s


class JSONDataNodeError(JSONDataError):
    """ Error on node, slightly different from key."""

    def __str__(self):
        return "JSONDataNodeError:" + self.s


class JSONDataNodeTypeError(JSONDataError):
    """ Error on NodeTypes."""

    def __str__(self):
        return "JSONDataNodeTypeError:" + self.s


class JSONDataParameterError(JSONDataError):
    """ Erroneous parameters."""

    def __str__(self):
        return "JSONDataParameterError:" + self.s


class JSONDataSourceFileError(JSONDataError):
    """ Error on read of a source file."""

    def __str__(self):
        return "JSONDataSourceFileError:" + self.s


class JSONDataModeError(JSONDataError):
    """ Type error of source file content."""

    def __str__(self):
        return "JSONDataModeError:" + self.s


class JSONDataTargetFileError(JSONDataError):
    """ Error on writing a file."""

    def __str__(self):
        return "JSONDataTargetFileError:" + self.s


class JSONDataValueError(JSONDataError):
    """ Error on a value."""

    def __str__(self):
        return "JSONDataValueError:" + self.s


class JSONDataAmbiguityError(Exception):
    """ Error ambiguity of provided parameters."""

    def __init__(self, requested, *sources):
        if _interactive:
            self.s = "Ambiguious input for:\n  " + str(requested)
            for sx in sources:
                self.s += "\n    " + str(sx)
        else:
            self.s = "Ambiguious input for:" + str(requested)
            for sx in sources:
                self.s += ":" + str(sx)
        Exception.__init__(self, self.s)

    def __str__(self):
        return "JSONDataAmbiguityError:" + self.s


class JSONPointerError(JSONDataError):
    """ Pointer error."""
    pass


class JSONPointerTypeError(JSONDataError):
    """ Pointer type error, the JSON pointer syntax does not represent a valid pointer."""
    pass


class JSONTypeError(JSONDataError):
    """ Pointer error."""
    pass


class JSONDiffError(JSONDataError):
    """Error in JSONDiff."""
    pass


class JSONSearchError(JSONDataError):
    """Error in JSONSearch."""
    pass


class JSONDataPatchError(JSONDataError):
    pass


class JSONDataPatchItemError(JSONDataPatchError):
    pass


#
# mode of operations
#
MJ_RFC4627 = 1  #: The first JSON RFC.
MJ_RFC7493 = 2  #: The IJSON RFC.
MJ_RFC7159 = 2  #: The JSON RFC by 'now'.
MJ_RFC8259 = 4  #: The JSON RFC by 'now'.
MJ_ECMA404 = 16  #: The first JSON EMCMA standard.
MJ_RFC6901 = 32  #: JSONPointer first IETF RFC.
MJ_RELPOINTERD1 = 64  #: JSONPointer - relative pointer Draft-1.
MJ_RFC6902 = 128  #: JSONPatch first IETF RFC.
MJ_DEFAULT = MJ_RFC7159

#
# validation of schemes
#
MS_OFF = 40  #: No validation.
MS_DRAFT3 = 43  #: The first supported JSONSchema IETF-Draft.
MS_DRAFT4 = 44  #: The current supported JSONSchema IETF-Draft.
MS_ON = MS_DRAFT4  #: The current when the default is activated.
MODE_SCHEMA_DEFAULT = MS_OFF  #: The current default validation mode.

str2mj = {
    "rfc4627": MJ_RFC4627,
    "rfc7493": MJ_RFC7493,
    "rfc7159": MJ_RFC7159,
    "rfc8259": MJ_RFC8259,
    "relpointerD1": MJ_RELPOINTERD1,
    "ecma404": MJ_ECMA404,
    "rfc6901": MJ_RFC6901,
    "rfc6902": MJ_RFC6902,
    "oss": MS_OFF,
    str(MJ_RFC4627): MJ_RFC4627,
    str(MJ_RFC7493): MJ_RFC7493,
    str(MJ_RFC7159): MJ_RFC7159,
    str(MJ_RFC8259): MJ_RFC8259,
    str(MJ_ECMA404): MJ_ECMA404,
    str(MJ_RFC6901): MJ_RFC6901,
    str(MJ_RELPOINTERD1): MJ_RELPOINTERD1,
    str(MJ_RFC6902): MJ_RFC6902,
    str(MS_OFF): MS_OFF,
    MJ_RFC4627: MJ_RFC4627,
    MJ_RFC7493: MJ_RFC7493,
    MJ_RFC7159: MJ_RFC7159,
    MJ_ECMA404: MJ_ECMA404,
    MJ_RFC6901: MJ_RFC6901,
    MJ_RFC6902: MJ_RFC6902,
    MS_OFF: MS_OFF,
}
mj2str = {
    MJ_RFC4627: "rfc4627",
    MJ_RFC7493: "rfc7493",
    MJ_RFC7159: "rfc7159",
    MJ_RFC8259: "rfc8259",
    MJ_RELPOINTERD1: "relpointerD1",
    MJ_ECMA404: "ecma404",
    MJ_RFC6901: "rfc6901",
    MJ_RFC6902: "rfc6902",
    MS_OFF: "off",
}




#
# match criteria for node comparison
#
MATCH_INSERT = 0  #: for dicts
MATCH_NO = 1  #: negates the whole set
MATCH_KEY = 2  #: for dicts
MATCH_CHLDATTR = 3  #: for dicts and lists
MATCH_INDEX = 4  #: for lists
MATCH_MEM = 5  #: for dicts(value) and lists
MATCH_NEW = 6  #: If not present create a new, else ignore and keep present untouched.
MATCH_PRESENT = 7  #: Check all are present, else fails.


#
# application constraints and types for branch operations ::
#   res = a OP b
#
B_ALL = 0  #: OP-On-Branches: process in any case.
B_AND = 1  #: OP-On-Branches: process only when both present.
B_OR = 2  #: OP-On-Branches: process if one at all is present.
B_XOR = 4  #: OP-On-Branches: process if only one is present.

B_ADD = 8  #: OP-On-Branches: add in accordance to RFC6902
B_MOD = 16  #: OP-On-Branches: modulo of branches.
B_SUB = 32  #: OP-On-Branches: subtract branches.

#
# copy property
#
C_REF = 0  #: OP-Copy: Copy reference.
C_DEEP = 1  #: OP-Copy: Copy deep.
C_SHALLOW = 2  #: OP-Copy: Copy shallow.
C_DEFAULT = C_REF  #: Default value.


#
# application-scope
#
SC_DATA = 0  #: OP-Scope: the managed JSON data only
SC_SCHEMA = 1  #: OP-Scope: the managed JSON schema only
SC_JSON = 2  #: OP-Scope: the managed JSON data and schema only.
SC_OBJ = 3  #: OP-Scope: the attributes of current instance.
SC_ALL = 4  #: OP-Scope: the complete object, including data.


#
# data-scope
#
SD_BOTH = 0  #: Apply on mixed input and output data.
SD_INPUT = 1  #: Apply on input data.
SD_OUTPUT = 2  #: Apply on output data.


#
# sort order
#
S_NONE = 0  # no sort
S_SIMPLE = 1  # goups upper lower


#
# return types
#
R_OBJ = 0  #: Return object of type self.
R_DATA = 1  #: Return self.data.
R_JDATA = 2  #: Return object of type JSONData.

#
# types of return values
#
RT_STR = 1  #: string - 'str' or 'unicode'
RT_DICT = 2  #: dict
RT_LST = 4  #: list
RT_JSONPOINTER = 8  #: JSONPointer
RT_JSONPATCH= 16  #: JSONPatch
RT_JSONDATA = 32  #: JSONData
RT_DEFAULT = RT_JSONPOINTER  #: default
rtypes2num = {
    'RT_DICT': RT_DICT,
    'RT_JSONDATA': RT_JSONDATA,
    'RT_JSONPATCH': RT_JSONPATCH,
    'RT_JSONPOINTER': RT_JSONPOINTER,
    'RT_LST': RT_LST,
    'RT_STR': RT_STR,
    'default': RT_DEFAULT,
    'dict': RT_DICT,
    'jdata': RT_JSONPATCH,
    'jpatch': RT_JSONDATA,
    'jpointer': RT_JSONPOINTER,
    'list': RT_LST,
    'str': RT_STR,
    None: RT_DEFAULT,
    RT_DEFAULT: RT_DEFAULT,
    RT_DICT: RT_DICT,
    RT_JSONDATA: RT_JSONDATA,
    RT_JSONPATCH: RT_JSONPATCH,
    RT_JSONPOINTER: RT_JSONPOINTER,
    RT_LST: RT_LST,
    RT_STR: RT_STR,
}

#
# match sets
#
M_FIRST = 1  #: First match only.
M_LAST = 2  #: Last match only.
M_ALL = 4  #: All matches.


#
# verify pointers against jsondata
#
V_NONE = 1  #: no checks at all
V_FINAL = 2  #: checks final result only
V_STEPS = 4  #: checks each intermediate directory
V_DEFAULT = V_NONE  #: default
verify2num = {
    'V_DEFAULT': V_DEFAULT,
    'V_FINAL': V_FINAL,
    'V_NONE': V_NONE,
    'V_STEPS': V_STEPS,
    'default': V_DEFAULT,
    'final': V_FINAL,
    'none': V_NONE,
    'steps': V_STEPS,
    None: V_DEFAULT,
    V_DEFAULT: V_DEFAULT,
    V_FINAL: V_FINAL,
    V_NONE: V_NONE,
    V_STEPS: V_STEPS,
}

#
# display formats for JSONDiff
#
DF_SUMUP = 0   # short list
DF_CSV = 1     # csv, for now semicolon only
DF_JSON = 3    # JSON struture
DF_TABLE = 4   # table, for now fixed
DF_REVIEW = 5  # short for quick review format
DF_REPR = 6    # repr() - raw string, Python syntax
DF_STR = 7     # str() - formatted string, Python syntax

str2df = {
    'sumup': DF_SUMUP,
    'csv': DF_CSV,
    'json': DF_JSON,
    'review': DF_REVIEW,
    'repr': DF_REPR,
    'str': DF_STR,
    'tabble': DF_TABLE,
    str(DF_SUMUP): DF_SUMUP,
    str(DF_CSV): DF_CSV,
    str(DF_JSON): DF_JSON,
    str(DF_REVIEW): DF_REVIEW,
    str(DF_REPR): DF_REPR,
    str(DF_STR): DF_STR,
    str(DF_TABLE): DF_TABLE,
    DF_SUMUP: DF_SUMUP,
    DF_CSV: DF_CSV,
    DF_JSON: DF_JSON,
    DF_REVIEW: DF_REVIEW,
    DF_REPR: DF_REPR,
    DF_STR: DF_STR,
    DF_TABLE: DF_TABLE,
}
df2str = {
    DF_SUMUP: 'sumup',
    DF_CSV: 'csv',
    DF_JSON: 'json',
    DF_REVIEW: 'review',
    DF_REPR: 'repr',
    DF_STR: 'str',
    DF_TABLE: 'tabble',
}

#
# display formats for JSONData
#
PJ_TREE = 0     #: tree view JSON syntax
PJ_FLAT = 1     #: flat print JSON syntax
PJ_PYTREE = 2   #: tree view Python syntax
PJ_PYFLAT = 3   #: flat print Python syntax
PJ_REPR = 4     #: repr() - raw string, Python syntax
PJ_STR = 5      #: str() - formatted string, Python syntax
str2pj = {
    'tree': PJ_TREE,
    'flat': PJ_FLAT,
    'pytree': PJ_PYTREE,
    'pyflat': PJ_PYFLAT,
    'repr': PJ_REPR,
    'str': PJ_STR,
    str(PJ_TREE): PJ_TREE,
    str(PJ_FLAT): PJ_FLAT,
    str(PJ_PYTREE): PJ_PYTREE,
    str(PJ_PYFLAT): PJ_PYFLAT,
    str(PJ_REPR): PJ_REPR,
    str(PJ_STR): PJ_STR,
    PJ_TREE: PJ_TREE,
    PJ_FLAT: PJ_FLAT,
    PJ_PYTREE: PJ_PYTREE,
    PJ_PYFLAT: PJ_PYFLAT,
    PJ_REPR: PJ_REPR,
    PJ_STR: PJ_STR,
}
pj2str = {
    PJ_TREE: 'tree',
    PJ_FLAT: 'flat',
    PJ_PYTREE: 'pytree',
    PJ_PYFLAT: 'pyflat',
    PJ_REPR: 'repr',
    PJ_STR: 'str',
}


#
# Notation at the API - in/out.
#
NOTATION_NATIVE = 0  #: JSON notation in accordance to RFC7159
NOTATION_JSON = 1  #: JSON notation in accordance to RFC7159
NOTATION_JSON_REL = 2  #: JSON notation as relative pointer
NOTATION_HTTP_FRAGMENT = 3  #: JSON notation in accordance to RFC7159 with RFC3986.


#
# character display
#
CHARS_RAW = 0  #: display character set as raw
CHARS_STR = 1  #: display character set as str
CHARS_UTF = 2  #: display character set as utf


#
# line handling for overflow
#
LINE_CUT = 0  #: force line fit
LINE_WRAP = 1  #: wrap line in order to fit to length


#
# search parameters
#
SEARCH_FIRST = 0  #: Break display after first match.
SEARCH_ALL = 1  #: List all matches.


#
# pointer style
#
PT_PATH = 0  #: Displays a list of items.
PT_RFC6901 = 1  #: Displays rfc6901 strings.
PT_NODE = 2  #: Displays the node.


#
# json syntax
#
JSYN_NATIVE = 1  #: Literally in accordance to standards.
JSYN_PYTHON = 2  #: Python in-memory syntax representation.



# maps match strings and enums onto match-enums
match2match ={
    'child_attr_list': MATCH_CHLDATTR,
    'index': MATCH_INDEX,
    'key': MATCH_KEY,
    'mem': MATCH_MEM,
    'new': MATCH_NEW,
    'no': MATCH_NO,
    'present': MATCH_PRESENT,
    MATCH_CHLDATTR: MATCH_CHLDATTR,
    MATCH_INDEX: MATCH_INDEX,
    MATCH_KEY: MATCH_KEY,
    MATCH_MEM: MATCH_MEM,
    MATCH_NEW: MATCH_NEW,
    MATCH_NO: MATCH_NO,
    MATCH_PRESENT: MATCH_PRESENT,
}


# maps mode strings and enums onto mde-enums
mode2mj = {
    'default': MJ_RFC7159,
    'ecma404': MJ_RFC8259,
    'rfc4627': MJ_RFC4627,
    'rfc7159': MJ_RFC7159,
    'rfc7493': MJ_RFC7493,
    'rfc8259': MJ_RFC8259,
    MJ_ECMA404: MJ_RFC8259,
    MJ_RFC4627: MJ_RFC4627,
    MJ_RFC7159: MJ_RFC7159,
    MJ_RFC7493: MJ_RFC7493,
    MJ_RFC8259: MJ_RFC8259,
}


# maps validator strings and enums onto validator-enums
validator2ms = {
    'default': MS_DRAFT4,
    'draft3': MS_DRAFT3,
    'off': MS_OFF,
    MS_DRAFT3: MS_DRAFT3,
    MS_DRAFT4: MS_DRAFT4,
    MS_OFF: MS_OFF,
}


# maps copy strings and enums onto copy-enums
copy2c = {
    'deep': C_DEEP,
    'default': C_REF,
    'ref': C_REF,
    'shallow': C_SHALLOW,
    C_DEEP: C_DEEP,
    C_REF: C_REF,
    C_SHALLOW: C_SHALLOW,
}


#
# for now hard-coded
#
consolewidth = 80

#
# misc
#
_verbose = 0  # common verbose variable
_debug = 0  # common verbose variable

