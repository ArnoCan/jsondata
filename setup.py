# -*- coding: utf-8 -*-
"""Distribute 'jsondata', a bytecode compilation and raw import.
   Based on 'py_compile' and 'importlib'.

   Installs 'jsondata', adds/modifies the following helper features
   to standard 'setuptools' options.

   Args:

      build_apydoc

        Creates standalone documentation similar to
        javadoc by Apydoc, html only.

        Supports Python 2.7+ and 3.5+.

      build_doc

        Creates Sphinx based documentation with embeded
        javadoc-style API documentation, html only.

      build_apydoc

        Creates standalone documentation for runtime
        system by Apydoc, html only.

      build_epydoc

        Creates standalone documentation for runtime
        system by Epydoc, html only.

      build_sphinx

        Creates documentation for runtime system by
        Sphinx, html only. Calls 'callDocSphinx.sh'.

      docdist

        Creates documentation package as 'tar.gz'
        and 'zip' archive in 'dist'.

      project_doc

        Install a local copy into the 'doc' directory
        of the project.

      instal_doc

        Install a local copy of the previously build
        documents in accordance to PEP-370.

      test

        Runs PyUnit tests by discovery.

      usecases

        Runs PyUnit UseCases by discovery, a lightweight
        set of unit tests.

    Options:

        For "setup.py install [<options>] [<pyparargs-options>] ..."

          --sdk

            Requires sphinx, epydoc, and dot-graphics.

          --no-install-required

            Suppresses installation dependency checks,
            requires appropriate PYTHONPATH.

          --offline

            Sets online dependencies to offline, or ignores
            online dependencies.

          --exit

            Exit 'setup.py'.

          --help-jsondata

            Displays this help.

   Returns:
      Results for success in installed 'jsondata'.

   Raises:
      passes-through

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from setuptools import setup  # , find_packages
import fnmatch
import shutil
import tempfile
import re

__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010,2011,2015-2017 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.22'
__uuid__ = '32f6017b-8b45-48f9-bafe-b00319228d54'

_NAME = 'jsondata'

# some debug
if __debug__:
    __DEVELTEST__ = True


version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '3.5' and version not in ('2.7',):
    raise Exception("Requires Python-2.7, or >=3.5")

#
# required for a lot for now, thus just do it
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


_epydoc = "apydoc"
_epydoc = "epydoc"


def find_files(srcdir, *wildcards, **kw):
    """Assembles a list of package files for package_files.

        Args:
            srcdir: Source root.
            *wildcards: list of globs.
            **kw: Additional control of resolution:
                single_level: Flat only.
                subpath: Cut topmost path elemenr from listelements,
                    special for dictionaries.
                nopostfix: Drop filename postfix.
                packages: List packages only, else files.
                yield_folders:
        Returns:
            Results in an list.

        Raises:
            ffs.

    """
    def all_files(root, *patterns, **kw):
        ret = []
        single_level = kw.get('single_level', False)
        subpath = kw.get('subpath', False)
        nopostfix = kw.get('nopostfix', True)
        packages = kw.get('packages', True)
        yield_folders = kw.get('yield_folders', True)

        for path, subdirs, files in os.walk(root):
            if yield_folders:
                files.extend(subdirs)
            files.sort()

            if subpath:
                path = re.sub(r'^[^' + os.sep + ']*' + os.sep, '', path)

            for name in files:
                if name in ('.gitignore', '.git', '.svn'):
                    continue

                for pattern in patterns:
                    if fnmatch.fnmatch(name, pattern):
                        if packages:
                            if not name == '__init__.py':
                                continue
                            ret.append(path)
                            continue
                        if nopostfix:
                            name = os.path.splitext(name)[0]

                        ret.append(os.path.join(path, name))

            if single_level:
                break
        return ret

    file_list = all_files(srcdir, *wildcards, **kw)
    return file_list


def usage():
    if __name__ == '__main__':
        import pydoc
        print(pydoc.help(__name__))
    else:
        help(str(os.path.basename(sys.argv[0]).split('.')[0]))

#
# * shortcuts
#


exit_code = 0

# custom doc creation by sphinx-apidoc
if 'build_sphinx' in sys.argv or 'build_doc' in sys.argv:
    try:
        os.makedirs('build' + os.sep + 'apidoc' + os.sep + 'sphinx')
    except:
        pass

    print("#---------------------------------------------------------")
    exit_code = os.system('./callDocSphinx.sh')  # create apidoc
    print("#---------------------------------------------------------")
    print("Called/Finished callDocSphinx.sh => exit=" + str(exit_code))
    if 'build_sphinx' in sys.argv:
        sys.argv.remove('build_sphinx')

# common locations
src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
dst0 = os.path.normpath("build/apidoc/" + str(_NAME))

# custom doc creation by sphinx-apidoc with embeded epydoc
if 'build_doc' in sys.argv:

    # copy sphinx to mixed doc
    if not os.path.exists(src0):
        raise Exception("Missing generated sphinx document source:" +
                        str(src0))
    if os.path.exists(dst0):
        shutil.rmtree(dst0)
    shutil.copytree(src0, dst0)

    print("#---------------------------------------------------------")
    exit_code = os.system(str(_epydoc) + ' --config docsrc/' + str(_epydoc) + '.conf')
    print("#---------------------------------------------------------")
    print("Called/Finished " + str(_epydoc) + " --config docsrc/" + str(_epydoc) + ".conf => exit=" +
          str(exit_code))

    def _sed(filename, pattern, repl, flags=0):
        pattern_compiled = re.compile(pattern, flags)
        fname = os.path.normpath(filename)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as ftmp:
            with open(fname) as src_file:
                for line in src_file:
                    ftmp.write(pattern_compiled.sub(repl, line))

        shutil.copystat(fname, ftmp.name)
        shutil.move(ftmp.name, fname)

    pt = '<a target="moduleFrame" href="toc-everything.html">Everything</a>'
    rp = r'<a href="../index.html" target="_top">Home</a>'
    rp += r' - '
    rp += r'<a href="./index.html" target="_top">Top</a>'
    rp += r' - '
    rp += pt

    fn = dst0 + '/' + str(_epydoc) + '/toc.html'
    _sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable

    pt = '[@]local-manuals'
    rp = r'[<a href="../index.html#table-of-contents" target="_top">@local-manuals</a>'
    for flst in os.walk(dst0 + '/' + str(_epydoc) + '/'):
        for fn in flst[2]:
            if fn[-5:] == '.html':
                _sed(flst[0] + os.path.sep + fn, pt, rp, re.MULTILINE)  # @UndefinedVariable

    pt = '[&][#]64[;]local-manuals'
    rp = r'@[<a href="../index.html#table-of-contents" target="_top">local-manuals</a>]'
    for flst in os.walk(dst0 + '/' + str(_epydoc) + '/'):
        for fn in flst[2]:
            if fn[-5:] == '.html':
                _sed(flst[0] + os.path.sep + fn, pt, rp, re.MULTILINE)  # @UndefinedVariable
    pt = re.compile(
        r'(<span class="codelink"><a href=.*jsondata[.])([^\\-]+)([\\-][^#]*[#])([^"]+)(">source&nbsp;code</a></span>)'
        )

    def rpfunc(match):
        rp = r'[<span class="codelink"><a href="../' + match.group(2).lower() + '.html#' + match.group(4).lower() + '" target="_top">api</a></span>]&nbsp;'

        rp += match.group(1) + match.group(2) + match.group(3) + match.group(4) + match.group(5)

        return rp
    for flst in os.walk(dst0 + '/' + str(_epydoc) + '/'):
        for fn in flst[2]:
            if fn[-5:] == '.html':
                _sed(flst[0] + os.path.sep + fn, pt, rpfunc)

    pt = '<h4>Next topic</h4>'
    rp = r'<h4>API</h4><p class="topless"><a href="' + str(_epydoc) + '/index.html" title="API">Programming Interface</a></p>'
    rp += pt
    fn = dst0 + '/index.html'
    _sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable

    pt = r'<li><a class="reference internal" href="#table-of-contents">Table of Contents</a></li>'
    rp = r'<li><a class="reference internal" href="shortcuts.html">Shortcuts</a></li>'
    rp += r'<li><a class="reference internal" href="howto.html">Howto</a></li>'
    rp += r'<li><a class="reference internal" href="install.html">Install</a></li>'
    rp += pt
    fn = dst0 + '/index.html'
    _sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable

    pt = '<h4>Previous topic</h4>'
    rp = r'<h4>API</h4><p class="topless"><a href="' + str(_epydoc) + '/index.html" title="API">Programming Interface</a></p>'
    rp += pt
    patchlist = [
        'shortcuts.html',
        'jsondata.html',
    ]
    for px in patchlist:
        fn = dst0 + os.sep + px
        _sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable

#     pt = '<h3>Quick search</h3>'
#     rp = r'<h4>API</h4><p class="topless"><a href="../../' + str(_epydoc) + '/index.html" title="API">Programming Interface</a></p>'
#     rp += pt
#     patchlist = [
#         '_modules/jsondata/SubprocessCall.html',
#     ]
#     for px in patchlist:
#         fn = dst0 + os.sep + px
#         _sed(fn, pt, rp, re.MULTILINE)

    sys.argv.remove('build_doc')

if 'build_' + str(_epydoc) + '' in sys.argv:
    try:
        os.makedirs('build' + os.sep + 'apidoc' + os.sep + 'apydoc')
    except:
        pass

    print("#---------------------------------------------------------")
    exit_code = os.system(str(_epydoc) + ' --config docsrc/' + str(_epydoc) + '-standalone.conf')
    print("#---------------------------------------------------------")
    print(
        "Called/Finished " + str(_epydoc) + " --config docsrc/" + str(_epydoc) + "-standalone.conf => exit=" +
        str(exit_code)
        )
    sys.argv.remove('build_' + str(_epydoc))

# install local project doc
if 'project_doc' in sys.argv:
    print("# project_doc.sh...")

    dstroot = os.path.normpath("doc/en/html/man3/") + os.sep

    try:
        os.makedirs(dstroot)
    except:
        pass

    if os.path.exists(dst0):
        if os.path.exists(dstroot + str(_NAME)):
            shutil.rmtree(dstroot + str(_NAME))
        shutil.copytree(dst0, dstroot + str(_NAME))

    src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".sphinx"):
            shutil.rmtree(dstroot + str(_NAME) + ".sphinx")
        shutil.copytree(src0, dstroot + str(_NAME) + ".sphinx")

    src0 = os.path.normpath("build/apidoc/" + str(_epydoc))
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".apydoc"):
            shutil.rmtree(dstroot + str(_NAME) + ".apydoc")
        shutil.copytree(src0, dstroot + str(_NAME) + ".apydoc")

    print("#")
    idx = 0
    for i in sys.argv:
        if i == 'install_doc':
            break
        idx += 1

    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    sys.argv.remove('project_doc')

# install user doc
if 'install_doc' in sys.argv:
    print("# install_doc...")

    # set platform
    if sys.platform in ('win32'):
        dstroot = os.path.expandvars("%APPDATA%/Python/doc/en/html/man3/")
    else:
        dstroot = os.path.expanduser("~/.local/doc/en/html/man3/")
    dstroot = os.path.normpath(dstroot) + os.sep

    try:
        os.makedirs(dstroot)
    except:
        pass

    if os.path.exists(dst0):
        if os.path.exists(dstroot + str(_NAME)):
            shutil.rmtree(dstroot + str(_NAME))
        shutil.copytree(dst0, dstroot + str(_NAME))

    src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".sphinx"):
            shutil.rmtree(dstroot + str(_NAME) + ".sphinx")
        shutil.copytree(src0, dstroot + str(_NAME) + ".sphinx")

    src0 = os.path.normpath("build/apidoc/epydoc")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + "." + str(_epydoc)):
            shutil.rmtree(dstroot + str(_NAME) + "." + str(_epydoc))
        shutil.copytree(src0, dstroot + str(_NAME) + "." + str(_epydoc))

    print("#")
    idx = 0
    for i in sys.argv:
        if i == 'install_doc':
            break
        idx += 1

    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    sys.argv.remove('install_doc')

# install local project doc
if 'install_project_doc' in sys.argv:
    print("# project_doc.sh...")

    dstroot = os.path.normpath("doc/en/html/man3/")+os.sep

    try:
        os.makedirs(dstroot)
    except:
        pass

    if os.path.exists(dst0):
        if os.path.exists(dstroot+str(_NAME)):
            shutil.rmtree(dstroot+str(_NAME))
        shutil.copytree(dst0, dstroot+str(_NAME))


    src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
    if os.path.exists(src0):
        if os.path.exists(dstroot+str(_NAME)+".sphinx"):
            shutil.rmtree(dstroot+str(_NAME)+".sphinx")
        shutil.copytree(src0, dstroot+str(_NAME)+".sphinx")

    src0 = os.path.normpath("build/apidoc/epydoc")
    if os.path.exists(src0):
        if os.path.exists(dstroot+str(_NAME)+".epydoc"):
            shutil.rmtree(dstroot+str(_NAME)+".epydoc")
        shutil.copytree(src0, dstroot+str(_NAME)+".epydoc")

    print("#")
    idx = 0
    for i in sys.argv:
        if i == 'install_project_doc': break
        idx += 1

    print("#")
    print("Called/Finished PyUnit tests => exit="+str(exit_code))
    print("exit setup.py now: exit="+str(exit_code))
    sys.argv.remove('install_project_doc')

# create tar.gz and zip for user doc
if 'docdist' in sys.argv:
    print("# docdist...")

    src0 = os.path.normpath("build/apidoc/"+_NAME)
    if not os.path.exists(src0):
        raise Exception("Requires pre-built documents in 'doc' by 'build_doc'")
    if not os.path.exists("dist"):
        os.mkdir('dist')

    _archname = _NAME + "-doc" + "-" + __version__
    src1 = os.path.normpath("build/apidoc/"+_archname)
    if os.path.exists(src1):
        shutil.rmtree(src1)
    shutil.copytree(src0, src1)

    _targz_archpathname = "dist" + os.path.sep + _archname + ".tar.gz"
    _call = "tar -C "+str(os.path.dirname(src1)) + " -cvf " \
        + str(_targz_archpathname) + " " + str(os.path.basename(src1))

    exit_code = os.system(_call)

    _zip_archpathname = "dist" + os.path.sep + _archname + ".zip"
    _call = "zip -r "+str(_zip_archpathname)+" "+str(src1)
    exit_code = os.system(_call)

    sys.argv.remove('docdist')

version = '{0}.{1}'.format(*sys.version_info[:2])

# call of complete test suite by 'discover'
if 'tests' in sys.argv or 'test' in sys.argv:
    if os.path.dirname(__file__) + os.pathsep not in os.environ['PATH']:
        p0 = os.path.dirname(__file__)
        os.putenv('PATH', p0 + os.pathsep + os.getenv('PATH', ''))
        print("# putenv:PATH[0]=" + str(p0))

    print("#")
    if version == '2.6':  # pragma: no cover
        print("# Check 'inspect' paths - call in: tests")
        exit_code = os.system('python -m discover -s tests -p CallCase.py')
        print("# Check 'inspect' paths - call in: tests.30_libs")
        exit_code += os.system(
            'python -m discover -s tests.30_libs -p CallCase.py'
            )
        print(
            "# Check 'inspect' paths - call in: tests.30_libs.040_jsondata"
            )
        exit_code += os.system(
            'python -m discover -s tests.30_libs.040_jsondata -p CallCase.py'
            )
    elif version == '2.7':  # pragma: no cover
        print("# Check 'inspect' paths - call in: tests")
        exit_code = os.system(
            'python -m unittest discover -s tests -p CallCase.py'
            )
        print("# Check 'inspect' paths - call in: tests.30_libs")
        exit_code += os.system(
            'python -m unittest discover -s tests.30_libs -p CallCase.py'
            )
        print(
            "# Check 'inspect' paths - call in: tests.30_libs.040_jsondata"
            )
        exit_code += os.system(
            'python -m unittest discover -s tests.30_libs.040_jsondata -p CallCase.py'
            )
    else:
        sys.stderr.write("ERROR:Version not supported:" + str(version))
        sys.exit(1)
    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    try:
        sys.argv.remove('test')
    except:
        pass
    try:
        sys.argv.remove('tests')
    except:
        pass

# call of complete UseCases by 'discover'
if 'usecases' in sys.argv or 'usecase' in sys.argv:
    if os.path.dirname(__file__) + os.pathsep not in os.environ['PATH']:
        p0 = os.path.dirname(__file__)
        os.putenv('PATH', p0 + os.pathsep + os.getenv('PATH', ''))
        print("# putenv:PATH[0]=" + str(p0))

    print("#")
    if version == '2.6':  # pragma: no cover
        print("# Check 'inspect' paths - call in: UseCases")
        exit_code = os.system('python -m discover -s UseCases -p CallCase.py')
        print("# Check 'inspect' paths - call in: UseCases.jsondata")
        exit_code += os.system(
            'python -m discover -s UseCases.jsondata -p CallCase.py'
            )
    elif version == '2.7':  # pragma: no cover
        print("# Check 'inspect' paths - call in: UseCases")
        exit_code = os.system(
            'python -m unittest discover -s UseCases -p CallCase.py'
            )
        print("# Check 'inspect' paths - call in: UseCases.jsondata")
        exit_code += os.system(
            'python -m unittest discover -s UseCases.jsondata -p CallCase.py'
            )
    else:
        sys.exit(1)
    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    try:
        sys.argv.remove('usecase')
    except:
        pass
    try:
        sys.argv.remove('usecases')
    except:
        pass

__sdk = False
if '--sdk' in sys.argv:
    __sdk = True
    sys.argv.remove('--sdk')

# Intentional HACK: ignore (online) dependencies, mainly
#    foreseen for developement
__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

# Intentional HACK: offline only, mainly foreseen for developement
__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')

# Execution failed - Error.
if exit_code != 0:
    sys.exit(exit_code)

# Help on addons.
if '--help-jsondata' in sys.argv:
    usage()
    sys.exit(0)

# Exit here.
if '--exit' in sys.argv:
    sys.exit(0)

# if jsondata-specials only
if len(sys.argv) == 1:
    sys.exit(exit_code)

_name = _NAME

_description = (
    "Provides integrated JSON Data(RFC7159), Pointer(RFC6901), Relative Pointer(draft-handrews-relative-json-pointer)," 
    "Patch(RFC6902), and modular JSON branch management with set operators."
   )

_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read()

_platforms = 'any'

_classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: Free To Use But Restricted",
    "License :: OSI Approved :: Artistic License",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: OS Independent",
    "Operating System :: POSIX :: BSD :: OpenBSD",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: SunOS/Solaris",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Unix Shell",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]

_keywords = ' Python PyPy stackless '
_keywords += ' JSON JSONPointer Pointer JSONPatch Patch Relative Pointer Relative-Pointer'
_keywords += ' RFC7159 RFC4627 RFC6901 RFC6902'
_keywords += ' json ujson jsonschema jsondata'
_keywords += ' Python2 Python3'
_keywords += ' parallel multi-processing multipstreading '

_packages = ["jsondata"]
_scripts = []

_package_data = {
    'jsondata': ['README.md', 'ArtisticLicense20.html', 'LICENSE',
                   'licenses-amendments.txt',
                   'doc'
                   ],
}

# _download_url="https://github.com/ArnoCan/jsondata/"
_download_url = "https://sourceforge.net/projects/jsondata/files/"

_url = 'https://sourceforge.net/projects/jsondata/'


# common
_install_requires = [
    'pysourceinfo >= 0.1.20',
    'filesysobjects >= 0.1.20',
]

# if sys.platform is 'win32':
#     # win32
#     _install_requires.extend(
#         [
#             'win32pipe',
#             'win32file',
#             'msvcrt'
#         ]
#     )
# else:
#     # else
#     _install_requires.extend(
#         [
#             'select',
#             'fcntl',
#         ]
#     )

if __sdk:  # pragma: no cover
    _install_requires.extend(
        [
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )

_test_suite = "tests.CallCase"

if __debug__:
    if __DEVELTEST__:
        print("#---------------------------------------------------------")
        print("packages=" + str(_packages))
        print("#---------------------------------------------------------")
        print("package_data=" + str(_package_data))
        print("#---------------------------------------------------------")

# Intentional HACK: ignore (online) dependencies, mainly
#     foreseen for developement
if __no_install_requires:
    print("#")
    print("# Changed to offline mode, ignore install dependencies completely.")
    print("# Requires appropriate PYTHONPATH.")
    print("# Ignored dependencies are:")
    print("#")
    for ir in _install_requires:
        print("#   " + str(ir))
    print("#")
    _install_requires = []

#
setup(name=_name,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    classifiers=_classifiers,
    description=_description,
    download_url=_download_url,
    install_requires=_install_requires,
    keywords=_keywords,
    license=__license__,
    long_description=_long_description,
    platforms=_platforms,
    url=_url,
    scripts=_scripts,
    packages=_packages,
    package_data=_package_data,
    zip_safe=False, 
    )

if '--help-commands' in sys.argv:
    print()
    print("Extensions by '" + str(_NAME) + "':")
    print("  build_doc         create Sphinx based documentation")
    print("  build_apydoc      create Apydoc standalone documentation")
    print("  build_epydoc      create Epydoc standalone documentation")
    print("  docdist           create document archives in dist: tar.gz + zip")
    print("  instal_doc        install in accordance to PEP-370")
    print("  project_doc       install into project 'doc'")
    print("  test              runs PyUnit tests by discovery")
    print("  usecases          runs PyUnit UseCases by discovery")
    print()

if '--help' in sys.argv:
    print()
    print("Help on usage extensions by " + str(_NAME))
    print("   --help-" + str(_NAME))
    print("   --help-commands")
    print()
