function [y,z]=f(a,b)
    y = a+2
    z = b-3
end
function g()
    a = [1,2,3]
    b = [4;5;6]
    [y,z] = f(a,b)
end
