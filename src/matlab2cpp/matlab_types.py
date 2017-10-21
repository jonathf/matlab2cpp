import os
import shutil #copy files from current dir to m2cpp_temp
#import re
import matlab2cpp.mwhos
from matlab2cpp.datatype import get_mem

from itertools import takewhile

def lstripped(s):
    return ''.join(takewhile(str.isspace, s))

#def rstripped(s):
#    return ''.join(reversed(tuple(takewhile(str.isspace, reversed(s)))))

#def stripped(s):
#    return lstripped(s), rstripped(s)

def mtypes(builder, args):

    #Current working directory
    src_dir = os.getcwd() + os.path.sep

    dst_dir = src_dir + "m2cpp_data_type_temp" + os.path.sep

    # Delete the temporary folder which the datatype info
    if os.path.isdir(dst_dir):
        shutil.rmtree(dst_dir)
    #if directory m2cpp_data_type_temp does not exist, create it
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)

    #copy file in directory to m2cpp_temp
    #If there are data files in directory, then they have to be copied, or abspath to datafiles in program
    src_file_dir = os.path.dirname(os.path.abspath(args.filename)) + os.path.sep
    src_files = os.listdir(os.path.dirname(os.path.abspath(args.filename)) + os.path.sep)

    for file_name in src_files:
        file_src = src_file_dir + file_name
        if os.path.isfile(file_src):
            if file_src[-2:] != ".m":
                shutil.copy(file_src, dst_dir)

    #write whos_f.m to folder. Similar to matlab whos function,
    #but writes to file
    f = open(dst_dir + "whos_f.m", "w")
    f.write(matlab2cpp.mwhos.code)
    f.close()

    ##Create new matlab file in m2cpp_temp
    #Loop for each script and function .m file
    #print("- Program loop start\n\n")
    for program in builder.project:
        #get program code from matlab file
        f = open(program.name, "r")
        code = f.read()
        f.close()

        #Get name of file after splitting path, set file path "m2cpp_temp/file"
        file_path = dst_dir + program.name.split(os.path.sep)[-1]
        #print(file_path)

        #Program is main script file, add whos_f at end of file
        #program[1][0].cls is Main if script file
        if program[1][0].cls == "Main":
            #Modify the code, main file
            file_name = (program.name.split(os.path.sep)[-1])[:-2]
            code += "\nwhos_f"
        else:
            #Modify the code, funtion file
            code = function_code(program, code)

        #insert whos_f before return statements
        func_name = "whos_f"

        lines = code.splitlines()
        code_temp = []
        for line in lines:
            #lstrip line and compare with "return"
            if line.lstrip()[:6] == "return":
                #Insert left stripped whitespace + func_name
                code_temp.append(lstripped(line) + func_name)
            #Add the "original" code line
            code_temp.append(line)

        #Convert string list to string
        code = "\n".join(code_temp)
        
        #write file to m2cpp_temp/
        #print("writing file: " + file_path)

        f = open(file_path, "w")
        f.write(code)
        f.close()
    try:
        import matlab.engine

        #Set path to -p "setpath.m" before changing current working directory
        if args.paths_file:
            matlab_cmd = "run(\'"+ os.path.abspath(args.paths_file).rstrip(".m") + "\')"

        cwdir = os.getcwd()
        os.chdir(dst_dir)
        engine = matlab.engine.start_matlab()

        if args.paths_file:
            engine.evalc(matlab_cmd, nargout=0)
        engine.evalc(file_name, nargout=0)

        os.chdir(cwdir)
    except:
        print("matlab did not load correctly, check that you have matlab engine API for python installed")

    ##Process .m.txt files to extract data types
    #I could have this under the previous loop,
    #but then the loop becomes so long
    program_number = 0

    for program in builder.project:
        #reset funcs_types dictionary for each iteration
        funcs_types = {}
        file_path = dst_dir + program.name.split(os.path.sep)[-1] + ".txt"
        #print(file_path)
        funcs_types = extract_ftypes(program, funcs_types, file_path)
    
        ##Copy data types to program.ftypes
        funcs = program.ftypes

        for func_key in funcs_types.keys():
            for var_key in funcs_types[func_key].keys():
                funcs[func_key][var_key] = funcs_types[func_key][var_key]
        
        #set ftypes for the current program
        builder[program_number].ftypes = funcs
        program_number += 1

    return builder
        


def extract_ftypes(program, funcs_types, file_path):
    
    #Check if file exists, if not return
    if not os.path.isfile(file_path):
        return funcs_types

    #Read file
    f = open(file_path, "r")
    lines = f.read().splitlines() #change to read, and then splitlines
    f.close()

    #while line
    j = 0
    while j < len(lines):
        line = lines[j]

        #print(str(j) + ":" + line)
        #When function is found, loop over variables and
        cols = line.split(":")
        #add them to dict funcs_types
        if cols[0] == "#function_name":
            #print(line)
            #funcs_name = cols[1].split(",")[0]

            f_names = cols[1].split(",")

            #funcs_name = f_names[0].lstrip() if not len(f_names) == 2 else f_names[1].lstrip()
            funcs_name = f_names[0].lstrip() if program[1][0].cls != "Main" else f_names[1].lstrip()
            
            #skip next line
            j += 2

            #make double indexed dictionary
            if not funcs_types.get(funcs_name):
                funcs_types[funcs_name] = {}
            while j < len(lines) and lines[j] != "":
                cols = lines[j].split(", ")

                #cols contain: name, size, class, complex, integer
                #extract variables to be more readable
                var_name = cols[0]
                
                #print(lines[j])
                #extract the type in string format
                data_type = datatype_string(cols)

                #print(var_name + ": " + data_type)

                #insert in dictionary
                #check if entry in dictionary exist
                data_type_old = funcs_types[funcs_name].get(var_name)

                #complex type should stay complex type
                if data_type_old:
                    #get if datatype is comples, then mem_value should be 4
                    #mem_value_old = get_mem(data_type_old)
                    mem_value_new = get_mem(data_type)
                    #print("mem_value_new: ")
                    #print(mem_value_new)
                    if mem_value_new == 4:
                        funcs_types[funcs_name][var_name] = data_type
                else:
                    funcs_types[funcs_name][var_name] = data_type

                j += 1
                
        j += 1
    
    return funcs_types

def datatype_string(cols):
    #Convert data from cols to a string, representing the datatype
    M, N = [int(s) for s in cols[1].split("x")]
    var_type = cols[2]
    complex_number = int(cols[3])
    integer = int(cols[4])

    data_type = ""
    if var_type == "double":
        #non complex
        if not complex_number:
            #scalar
            if M == 1 and N == 1:
                if integer:
                    data_type = "int"
                else:
                    data_type = "double"
                    
            #vec
            if M > 1 and N == 1:
                #data_type = "mat"
                data_type = "vec"
                    
            #rowvec
            if M == 1 and N > 1:
                #data_type = "mat"
                data_type = "rowvec"
                    
            #matrix
            if (M > 1 and N > 1) or M == 0 or N == 0: #if empty matrix, set to mat
                data_type = "mat"
                    
        #complex value
        elif complex_number:
            #scalar
            if M == 1 and N == 1:
                data_type = "cx_double"

            #vec
            if M > 1 and N == 1:
                #data_type = "cx_mat"
                data_type = "cx_vec"
                
            #rowvec
            if M == 1 and N > 1:
                #data_type = "cx_mat"
                data_type = "cx_rowvec"
                
            #matrix
            if M > 1 and N > 1 or M == 0 or N == 0: #if empty matrix, set to mat:
                data_type = "cx_mat"
                
    return data_type
    
def detect_string(code, k):

    import string

    if code[k] != "'":
        syntaxerror(k, "start of string character (')")

    if code[k-1] == ".":
        return False

    j = k-1
    while code[j] in " \t":
        j -= 1

    if code[j] in string.letters+string.digits+")]}_":

        # special cases
        if code[j-3:j+1] == "case":
            return True

        return False

    return True


def function_code(program, code):
    #print(program.summary())

    #count number of if, while, for, switch and number of end

    #Flatten nodes, count number of nodes of type if, while for
    #num_if = 0 #num_while = 0 #num_for = 0 #num_switch = 0
    import re
    iwfs_ends = 0
    
    nodes = program.flatten(False, True, False)

    for node in nodes: 
        if node.cls in ["If", "While", "For", "Switch"]:
            iwfs_ends += 1

    #print("iwfs_ends: " + str(iwfs_ends))
    
    #Get number of 'end' on separate lines
    

    iquote = [i for i in range(len(code)) if code[i] == '\'']
    istring = [i for i in iquote if detect_string(code, i)]
    string_ends = []
    
    #for i in istring:
    #    k = next(j for j in range(i + 1,len(code)) if code[j] == '\'' and (j + 1 == len(code) or code[j + 1] != '\''))
    #    string_ends.append(k)
    #    #code = code[:i + 1] + code[k:]

    #if len(istring) > 0:
    #    ncode = code[:istring[0] + 1]
    #    for i in range(len(istring) - 1):
    #        ncode += code[string_ends[i]:istring[i + 1] + 1]

    #    #if (string_ends[-1] + 1 < len(code)):
    #    ncode += code[string_ends[-1]:]
    #    code = ncode
    
    #lines = code.splitlines()
    #for i in range(0,len(lines)):
    #    #lines[i] = re.sub(r'\'(.+)\'',"''", lines[i])
    #    #lines[i] = re.sub(r'\"(.+)\"',"''", lines[i])
    #    lines[i] = lines[i].split('%')[0]
    #code = '\n'.join(lines)
    
    #esplit = code.replace(';', '\n').replace(',','\n').split()
    ##elines = esplit.splitlines()
    #num_end = 0
    #for t in esplit:
    #    if t == "end":
    #        num_end += 1
    #for line in elines:
    #    if line.strip() == "end":
    #        num_end += 1
        #print(line)

    
   
    

    #print("num_end: " + str(num_end))


    #insert whos_f before return and before function ..... (here)end (next fun)
    #Comparing num_end with num_if, num_while, num_for and switch case find if
    #functions are ending with "end" keyword or not.

    #flag set to true if functions end with end keyword
    #function_end = num_end > iwfs_ends

    #get number of functions in .m function file
    num_funcs = len(program[1])

    #insert whos_f before end of function or before new function
    func_name = "whos_f\n"

    ids = []

    for func in program[1]:
        block = func[3]
        block_end = block.cur + len(block.code)
        
        if block.is_end_terminated:
            fs = code.rfind("end", block.cur, block_end)
            ids.append(fs)
        else:
            ids.append(block_end)

    ids.sort()

    ncode = code[:ids[0]]

    for i in range(len(ids) - 1):
        ncode = ncode + func_name + code[ids[i]:ids[i+1]]
    ncode = ncode + func_name + code[ids[-1]:]
    code = ncode
    #functions end with end keyword
    #index = len(code)
    
    #index = len(lines)
    ##print(code)
    #if function_end:
    #    #should stop when num_funcs becomes zero
    #    while num_funcs:
    #        #search for keyword end
    #        #index = code.rfind("end", 0, index)
    #        index = next(i for i in range(index - 1,-1,-1) if lines[i].strip() == 'end')

    #        #add function name to code
    #        lines = lines[:index] + [func_name] + lines[index:]
    #        #index += len(func_name)

    #        #Search for previous function
    #        if num_funcs != 1:
    #            #index = code.rfind("\nfunction", 0, index)
    #            index = next(i for i in range(index - 1,-1,-1) if len(lines[i].split()) > 0 and lines[i].split()[0] == 'function')
    #        num_funcs -= 1
    #else:
    #    #function does not end with end keyword
    #    while num_funcs:
    #        #code = code[:index] + func_name + code[index:]
    #        lines = lines[:index] + [func_name] + lines[index:]

    #        if num_funcs != 1:
    #            #index = code.rfind("\nfunction", 0, index)
    #            index = next(i for i in range(index - 1,-1,-1) if len(lines[i].split()) > 0 and lines[i].split()[0] == 'function')
    #        num_funcs -= 1
        

    #print(code)
    #code = '\n'.join(lines)
    return code
