import os
import shutil #copy files from current dir to m2cpp_temp
#import re
import matlab2cpp.mwhos

from itertools import takewhile

def lstripped(s):
    return ''.join(takewhile(str.isspace, s))

#def rstripped(s):
#    return ''.join(reversed(tuple(takewhile(str.isspace, reversed(s)))))

#def stripped(s):
#    return lstripped(s), rstripped(s)

def mtypes(builder):
    dir_parts = builder.project[0].name.split(os.path.sep)[:-1]
    src_dir = ""

    for part in dir_parts:
        src_dir = src_dir + part + os.path.sep
    #src_dir = src_dir
    dst_dir = src_dir + "m2cpp_temp" + os.path.sep

    #if directory m2cpp_temp does not exist, create it
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)

    #copy file in directory to m2cpp_temp
    #print src_dir
    #print dst_dir
    src_files = os.listdir(src_dir)
    for file_name in src_files:
        full_file_name = os.path.join(src_dir, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dst_dir)
    
    #write whos_f.m to folder. Similar to matlab whos function,
    #but writes to file
    f = open(dst_dir + "whos_f.m", "w")
    f.write(matlab2cpp.mwhos.code)
    f.close()

    ##Create new matlab file in m2cpp_temp
    #Loop for each script and function .m file
    #print "- Program loop start\n\n"
    for program in builder.project:
        #get program code from matlab file
        f = open(program.name, "r")
        code = f.read()
        f.close()

        #Get name of file after splitting path, set file path "m2cpp_temp/file"
        file_path = dst_dir + program.name.split(os.path.sep)[-1]
        #print file_path

        #Program is main script file, add whos_f at end of file
        #program[1][0].cls is Main if script file
        if program[1][0].cls == "Main":
            #Modify the code, main file
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
        #print "writing file: " + file_path

        f = open(file_path, "w")
        f.write(code)
        f.close()

    try:
        import matlab.engine
        cwdir = os.getcwd()
        os.chdir(dst_dir)
        engine = matlab.engine.start_matlab()
        file = open(file_path, "r")
        file_name = (program.name.split(os.path.sep)[-1])[:-2]
        engine.eval(file_name, nargout=0)
        file.close()
        os.chdir(cwdir)
    except:
        print "matlab did not load correctly, check that you have matlab engine API for python installed"
        pass

    ##Process .m.txt files to extract data types
    #I could have this under the previous loop,
    #but then the loop becomes so long
    program_number = 0
    for program in builder.project:
        #reset funcs_types dictionary for each iteration
        funcs_types = {}
        file_path = dst_dir + program.name.split(os.path.sep)[-1] + ".txt"
        #print file_path
        funcs_types = extract_ftypes(funcs_types, file_path)
    
        ##Copy data types to program.ftypes
        funcs = program.ftypes
        for func_key in funcs_types.keys():
            for var_key in funcs_types[func_key].keys():
                funcs[func_key][var_key] = funcs_types[func_key][var_key]
        #print file_path
        #print funcs_types
        #print funcs

        #print "---------"
        #print funcs_types
        
        #set ftypes for the current program
        builder[program_number].ftypes = funcs
        program_number += 1
    
    return builder
        


def extract_ftypes(funcs_types, file_path):
    
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

        #print str(j) + ":" + line
        #When function is found, loop over variables and
        cols = line.split(":")
        #add them to dict funcs_types
        if cols[0] == "#function_name":
            #print line
            #funcs_name = cols[1].split(",")[0]

            f_names = cols[1].split(",")
            funcs_name = f_names[0].lstrip() if not len(f_names) == 2 else f_names[1].lstrip()
            
            
            #skip next line
            j += 2

            #make double indexed dictionary
            funcs_types[funcs_name] = {}
            while j < len(lines) and lines[j] != "":
                cols = lines[j].split(", ")

                #cols contain: name, size, class, complex, integer
                #extract variables to be more readable
                var_name = cols[0]
                
                #print lines[j]
                #extract the type in string format
                data_type = datatype_string(cols)

                #print var_name + ": " + data_type

                #insert in dictionary
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
                if integer:
                    data_type = "ivec"
                else:
                    data_type = "vec"
                    
            #rowvec
            if M == 1 and N > 1:
                if integer:
                    data_type = "irowvec"
                else:
                    data_type = "rowvec"
                    
            #matrix
            if M > 1 and N > 1:
                if integer:
                    data_type = "imat"
                else:
                    data_type = "mat"
                    
        #complex value
        elif complex_number:
            #scalar
            if M == 1 and N == 1:
                data_type = "cx_double"

            #vec
            if M > 1 and N == 1:
                data_type = "cx_vec"
                
            #rowvec
            if M == 1 and N > 1:
                data_type = "cx_rowvec"
                
            #matrix
            if M > 1 and N > 1:
                data_type = "cx_mat"
                
    return data_type
    
def function_code(program, code):
    #print program.summary()

    #count number of if, while, for, switch and number of end

    #Flatten nodes, count number of nodes of type if, while for
    #num_if = 0 #num_while = 0 #num_for = 0 #num_switch = 0
    iwfs_ends = 0
    
    nodes = program.flatten(False, True, False)

    for node in nodes: 
        if node.cls in ["If", "While", "For", "Switch"]:
            iwfs_ends += 1

    #print "iwfs_ends: " + str(iwfs_ends)
    
    #Get number of 'end' on separate lines
    num_end = 0
    lines = code.splitlines()
    for line in lines:
        if line == "end":
            num_end += 1
        #print line

    #print "num_end: " + str(num_end)


    #insert whos_f before return and before function ..... (here)end (next fun)
    #Comparing num_end with num_if, num_while, num_for and switch case find if
    #functions are ending with "end" keyword or not.

    #flag set to true if functions end with end keyword
    function_end = num_end > iwfs_ends

    #get number of functions in .m function file
    num_funcs = len(program[1])

    #insert whos_f before end of function or before new function
    func_name = "whos_f\n"
    
    #functions end with end keyword
    index = len(code)
    #print code
    if function_end:
        #should stop when num_funcs becomes zero
        while num_funcs:
            #search for keyword end
            index = code.rfind("end", 0, index)

            #add function name to code
            code = code[:index] + func_name + code[index:]
            index += len(func_name)

            #Search for previous function
            if num_funcs != 1:
                index = code.rfind("\nfunction", 0, index)
            num_funcs -= 1
    else:
        #function does not end with end keyword
        while num_funcs:
            code = code[:index] + func_name + code[index:]

            if num_funcs != 1:
                index = code.rfind("\nfunction", 0, index)
            num_funcs -= 1
        

    #print code
    
    return code
