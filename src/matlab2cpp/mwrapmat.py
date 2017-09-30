try:
    import mlabraw
except:
    pass

class Wrapmat:
    #run matlab code with mlabraw
    def __init__(self):
        #get matlab session
        try:
            self.session = mlabraw.open()
        except Exception as e:      
            print("Error: %s" % str(e))
        
    def __del__(self):
        mlabraw.close(self.session)
    
    def eval_code(self, builder):
        self.builder = builder
    
        #should get a list of func names
        func_names = []
        for program in builder.project:
            print(program.summary())
            #flatten tree and find Func.names
            nodes = program.flatten(False, False, False)
            for node in nodes:
                if node.cls == "Func":
                    func_names.append(node.name)
        
        #print(func_names)
        self.func_names = func_names
        self.called_func_names = []
        
        #check if main
        func = builder[0][1][0]
        
        if func.name == 'main':
            code_block = func[3]
        
            #evaluate, recursive function
            self._evaluate(code_block)
            mlabraw.eval(self.session, 'whos_f')
        else:
            print('matlab have to run script file')
        
    def _evaluate(self, code_block):
        #eval line by line in code_block
        for node in code_block:
            func_nodes = []
            #multiline code -> for, while, if, case
            #if statement
            
            #one line code
            if node.cls in ('Assign', 'Assigns', 'Statement'):
                #flatten the node, check for function: Var/Get unknown type name
                sub_nodes = node.flatten(False, False, False)
                
                #check if Var/Get unknown type name -> self written function
                for sub_node in sub_nodes:
                    if ((sub_node.cls == 'Get' or sub_node.cls == 'Var') and \
                        sub_node.backend == 'unknown' and \
                        sub_node.type == 'TYPE' and \
                        sub_node.name in self.func_names):
                        
                        #Test if function processed before
                        if sub_node.name not in self.called_func_names:
                            func_nodes.append(sub_node)
                            self.called_func_names.append(sub_node.name)
                
                #loop over func_nodes
                for func_node in func_nodes:
                    #print(func_node.name)
                    params = []
                    function = False
                    
                    #save and store variables, if entered function
                    # node.func.name is name of caller function
                    mlabraw.eval(self.session, 'save mconvert_' + code_block.func.name)
                    
                    #clear variables, set params, Get function have params
                    mlabraw.eval(self.session, 'clear all')
                    
                    #find function node that is called
                    #check current file for function -> code_block
                    funcs = code_block.func.parent #funcs
                    for func in funcs:
                        if func_node.name == func.name:
                            new_code_block = func[3]
                            function = True
                    
                    #check other file for function -> code_block
                    if not function:
                        for program in node.project:
                            func = program[1][0]
                            if func_node.name == func.name:
                                params = func[2]
                                new_code_block = func[3]
                                function = True
                    
                    #set params
                    for var, param in zip(func_node, params):
                        my_string = "load (\'mconvert_" + code_block.func.name + "\', \'" + var.name + "\')"
                        mlabraw.eval(self.session, my_string)
                        
                        mlabraw.eval(self.session, param.name + ' = ' + var.name)

                        if var.name != param.name:
                            mlabraw.eval(self.session, 'clear ' + var.name)
                    
                    #jump into code_block of the function
                    self._evaluate(new_code_block)
                    
                    mlabraw.eval(self.session, 'whos_f')
                    #load previous variables
                    mlabraw.eval(self.session, 'clear all')
                    mlabraw.eval(self.session, 'load mconvert_' + code_block.func.name)
                    
            #eval code line
            mlabraw.eval(self.session, node.code)
