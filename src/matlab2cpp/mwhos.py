code=r"""function whos_f()
    %Static variables
    %persistent l %cellFile counter
    %persistent m %cellFunc counter
    %persistent cellFile
    %persistent cellFunc

    %initialize counter k
    %if isempty(l)
    %    l = 1;
    %    m = 1;
    %end

    %Get info about caller, filename
    ST = dbstack();
    if (length(ST) >= 2)
        file = strcat(ST(2).file, '.txt');
    else
        file = 'command_window.txt';
    end
    
    if (length(ST) > 2)
        func = ['#function_name: ', ST(2).name];
    elseif (length(ST) == 2)
        func = ['#function_name: ' , ST(2).name, ', main'];
    else
        func = '#command window:';
    end
    
    %should only run this function once for every function in file
    %if(~any(ismember(file, cellFile)) || ~any(ismember(func, cellFunc)))
        %Calls whos on caller workspace, then processes and prints the data
        cmdstr = 'whos;';
        my_vars = evalin('caller', cmdstr) ; 

        %numer of workspace variables
        Nvars = size(my_vars, 1);

        %fprintf('#name, size, class, complex, integer\n')
        str = sprintf('%s\n%s', func, '#name, size, class, complex, integer');
        for j = 1:Nvars
            %Test if all values are integer in variable, variable comes from caller workspace
            name = my_vars(j).name;
            cmd = ['all(' name ' == double(uint64(' name ')));'];
            
            %got error with struct, so I test if it works
            try
                integer = evalin('caller', cmd);
            catch
                integer = -1;
            end
            
            if (integer ~= -1)
                %Have to call all one more time for matrixes, two for cubes
                while (length(integer) > 1)
                    integer = all(integer); 
                end

                %Print the fields in the struct
                %fprintf('%s,%dx%d, %s, %d, %d\n', ...
                %        name, my_vars(j).size, my_vars(j).class, ...
                %        my_vars(j).complex, integer)
                temp = sprintf('\n%s, %dx%d, %s, %d, %d', ...
                                name, my_vars(j).size, my_vars(j).class, ...
                                 my_vars(j).complex, integer);
                str = [str, temp];
            end
        end

        %check if written to file, if not, new file, else append
        %if (~ismember(file, cellFile))
        %    cellFile{l} = file;
        %    l = l + 1;
        %    fp = fopen(file, 'w');
        %else
            fp = fopen(file, 'a');
            fprintf(fp, '\n');
        %end

        %add function to static cellarray cellFunc
        %cellFunc{m} = func; 
        %m = m + 1;
        
        %write whos to file
        fprintf(fp, '%s\n', str);
        fclose(fp);
    %end
end
"""
