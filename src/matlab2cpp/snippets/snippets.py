"""
Code snippets

Each snippit is on the form:
name = (kws, include, code)

where the name is used for retrieval, and

kws : dict
    Default values that will be used in interpelation (if not user provided).
include : str
    Code included in top of document (typically a for for include, if needed).
code : str
    Code included in suppliment '.h' file.
"""

complex = ({}, """#include <complex>
#include <cmath>""", "")

armadillo = ({}, """#include <armadillo>
using namespace arma ;""", "")

span = ({}, "",
"""arma::uvec span(int a, int step, int b)
{
arma::uvec s((arma::uword)0);
int n = (b - a + 1) / step;
if (n < 0)
{
return s;
}
s.set_size(n + 1);
for (int ii = 0; ii <= n; ii++)
{
s(ii) = step * ii + a;
}
return s;
}""")

nextpow2 = ({}, "",
"""inline int nextpow2(int n)
{
n = abs(n);
int p = 0;
int tmp = 1;
while (tmp < n)
{
tmp *= 2;
p++;
}
return p;
}""")


