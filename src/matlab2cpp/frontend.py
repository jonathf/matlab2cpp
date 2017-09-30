"""Execute main parser."""
import time
from datetime import datetime as date
import os
from os.path import sep
import imp

from . import supplement, tree, qfunctions, modify, setpaths
from .__init__ import __version__


def execute_parser(args):
    """
Initiate the interpretation and conversion process.

Args:
    args (ArgumentParser): arguments parsed through m2cpp
    """

    builder = tree.builder.Builder(
        disp=args.disp,
        comments=args.comments,
        original=args.original,
        enable_omp=args.enable_omp,
        enable_tbb=args.enable_tbb,
        reference=args.reference,
    )

    paths_from_file = []
    #read setpath.m file and return string list of paths
    if args.paths_file:
        if os.path.isfile(args.paths_file):
            paths_from_file = setpaths.multiple_folder_paths(args.paths_file)
        else:
            raise IOError("File '" + args.paths_file + "' not found")

    #pathOne = os.path.dirname(os.path.abspath(args.filename))

    if os.path.isfile(args.filename):

        paths = [os.path.abspath(os.path.dirname(args.filename))]
        paths += paths_from_file

        if args.disp:
            print("building tree...")

        filenames = [os.path.abspath(args.filename)]

        stack = []
        while filenames:

            filename = filenames.pop(0)
            assert os.path.isfile(filename)

            if filename in stack:
                continue

            if args.disp:
                print("loading", filename)

            stack.append(filename)

            f = open(filename, "rU")
            code = f.read()
            f.close()

            #code = re.sub('%#', '##', code)

            #Here you have to change filename to current folder for .py files
            #local_name = pathOne + sep + os.path.basename(filename)
            local_name = os.getcwd() + sep + os.path.basename(filename)

            if os.path.isfile(local_name + ".py") and not args.reset:

                try:
                    cfg = imp.load_source("cfg", local_name + ".py")

                except:
                    raise ImportError("""Supplement file:
    %s.py
    is formated incorrectly. Change the format or convert with '-r' option to create
    a new file.""" % local_name)

                if "verbatims" in cfg.__dict__ and cfg.verbatims:
                    verbatims = cfg.verbatims
                    code = supplement.verbatim.set(verbatims, code)

                builder.load(filename, code)
                program = builder[-1]

                if "functions" in cfg.__dict__:

                    funcs = program.ftypes

                    for name in funcs.keys():
                        if name in cfg.functions:
                            for key in cfg.functions[name].keys():
                                funcs[name][key] = cfg.functions[name][key]

                    program.ftypes = funcs

                if "structs" in cfg.__dict__:

                    structs = program.stypes

                    for name in structs.keys():
                        if name in cfg.structs:
                            for key in cfg.structs[name].keys():
                                structs[name][key] = cfg.structs[name][key]

                    program.stypes = structs

                if "includes" in cfg.__dict__:

                    includes = program.itypes

                    for key in cfg.includes:
                        if key not in includes:
                            includes.append(key)

                    includes = [i for i in includes if supplement.includes.write_to_includes(i)]

                    program.itypes = includes

            else:
                builder.load(filename, code)
                program = builder[-1]

            # add unknown variables to stack if they exists as files
            unknowns = builder.get_unknowns(filename)

            for i in xrange(len(unknowns)-1, -1, -1):
                #print(i)
                for path in paths:
                    #print(path)
                    if os.path.isfile(path + sep + unknowns[i] + ".m"):
                        unknowns[i] = unknowns[i] + ".m"
                    if os.path.isfile(path + sep + unknowns[i]):
                        program.include(path + sep + unknowns[i])
                        #filenames.append(path + sep + unknowns.pop(i))
                        filenames.append(path + sep + unknowns[i])


    else:
        builder.load("unnamed", args.filename)
        program = builder[-1]

    #--- work in progress ---
    #Run this mlabwrap code
    #Have this in a try-except block
    #import mwrapmat
    #wrapmat = mwrapmat.Wrapmat()
    #wrapmat.eval_code(builder)
    #------------------------

    #--- work in progress ---
    #Get data types from matlab
    if args.matlab_suggest:
        from . import matlab_types
        builder = matlab_types.mtypes(builder, args)
    #------------------------

    if args.disp:
        print("configure tree")

    builder.configure(suggest=(2*args.suggest or args.matlab_suggest))

    #--- work in progress ---
    #Modify the Abstract Syntax Tree (AST)
    builder.project = modify.preorder_transform_AST(
        builder.project, args.nargin,
        suggest=(2*args.suggest or args.matlab_suggest),
    )
    #------------------------

    if args.disp:
        print(builder.project.summary())
        print("generate translation")

    builder.project.translate(args)

    #post order modify project
    builder.project = modify.postorder_transform_AST(builder.project)

    t = time.time()
    stamp = date.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

    for program in builder.project:

        #name = program.name
        #if os.path.isfile(args.filename):
        #    name = pathOne + sep + os.path.basename(name)
            #print(name)
        name = os.getcwd() + sep + os.path.basename(program.name)
        #print(name)

        cpp = qfunctions.qcpp(program)
        hpp = qfunctions.qhpp(program)
        py = qfunctions.qpy(program, prefix=True)
        log = qfunctions.qlog(program)

        if args.disp:
            print("Writing files...")

        if args.reset:
            for ext in [".cpp", ".hpp", ".log", ".py"]:
                if os.path.isfile(name+ext):
                    os.remove(name+ext)

        if cpp:
            cpp = """// Automatically translated using m2cpp %s on %s

%s""" % (__version__, stamp, cpp)
            f = open(name+".cpp", "w")
            f.write(cpp)
            f.close()

        if hpp:
            hpp = """// Automatically translated using m2cpp %s on %s

%s""" % (__version__, stamp, hpp)
            f = open(name+".hpp", "w")
            f.write(hpp)
            f.close()

        if log:
            log = "Automatically translated using m2cpp %s on %s\n\n%s"\
                    % (__version__, stamp, log)
            f = open(name+".log", "w")
            f.write(log)
            f.close()

        if py:
            py = """# Automatically translated using m2cpp %s on %s
#
%s""" % (__version__, stamp, py)
            f = open(name+".py", "w")
            f.write(py)
            f.close()

        if os.path.isfile(name+".pyc"):
            os.remove(name+".pyc")


    program = builder[0]

    if args.tree_full:
        print(program.summary(args))

    elif args.tree:
        if program[1][0].cls == "Main":
            print(program[1][0][3].summary(args))
        else:
            print(program[1].summary(args))

    elif args.line:
        nodes = program[1].flatten(False, False, False)
        for node_ in nodes:
            if node_.line == args.line and node_.cls != "Block":
                print(node_.str.replace("__percent__", "%"))
                break
    else:
        print(program[1].str.replace("__percent__", "%"))
