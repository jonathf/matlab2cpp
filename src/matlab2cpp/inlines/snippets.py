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
    Code included in supplement '.h' file.

The value '%(file)s' will be substituted with the name of the file.
"""

armadillo = ({}, "#include <armadillo>", "")
namespace_arma = ({}, "using namespace arma ;", "")

span = ({}, '',
"""template <typename T>
inline arma::Row<typename T::elem_type> span(int a, int step, int b)
{
arma::Row<typename T::elem_type> s;
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

uspan = ({}, '',
"""inline arma::uvec uspan(int a, int step, int b)
{
arma::uvec s;
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

nextpow2 = ({}, '',
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

length = ({}, '',
"""template<typename T1>
arma::uword length(const T1& A)
{
return A.n_elem;
}""")

hankel = ({}, '',
"""template<typename T1, typename T2>
inline arma::Mat<typename T1::elem_type> hankel(const T1& c, const T2& r)
{
int nc = r.n_elem;
int nr = c.n_elem;
if (r[0] != c[0])
{
//("hankel: differing diagonal element. Using the column one");
}
arma::Mat<typename T1::elem_type> retval(nr, nc) = %(type)s;
for (int i = 1; i <= std::min(nr, nc); i++)
{
retval.submat(1-1, nr-i, i-1, i-1) = c.rows(i-1, nr-1);
}
int tmp = 1;
if (nc <= nr)
{
tmp = nr-nc+2;
}
for (int i = nr; i >= tmp; i--)
{
retval.submat(2+nr-i-1, nc-1, i-1, i-1) = arma::trans(r.cols(2-1, nc-nr+i-1));
}
return retval;
}""")

srow = ({}, '',
"""""")
scol = ({}, '',
"""""")
smat = ({}, '',
"""""")
scube = ({}, '',
"""""")

interp1 = ({}, "#include <matlib/interpolation.hpp>", "")

hpp = ({}, '#include "%(file)s.hpp"', "")
# ipp = ({}, '#include "%(file)s.ipp"', "")


extract = ({"struct" : "TYPE"}, '',
"""template<typename T>
inline arma::Vec<typename T::elem_type> extract(%(struct)s* s, int n)
{
arma::Vec<typename T::elem_type> out = arma::Vec<typename T::elem_type>(n);
for (int k=0; k<n; k++)
{
out(k) = s[k].%(value)s ;
}
return out ;
}""")

fft = ({}, "",
"""template <typename T>
inline arma::cx_mat fft(arma::Mat<typename T::elem_type> X, int dim)
{
if (dim == 1)
X = arma::fft(X) ;
else
X = arma::trans(arma::fft(arma::trans(X))) ;
return X ;
}
""")

fftn = ({}, "",
"""template <typename T>
inline arma::cx_mat fft(arma::Mat<typename T::elem_type> X, int n, int dim)
{
if (dim == 1)
X = arma::fft(X, n) ;
else
X = arma::trans(arma::fft(arma::trans(X)), n) ;
return X ;
}
""")

ifft = ({}, "",
"""template <typename T>
inline arma::Mat<typename T::elem_type> ifft(arma::cx_mat X, int dim)
{
if (dim == 1)
X = arma::ifft(X) ;
else
X = arma::trans(arma::ifft(arma::trans(X))) ;
return X ;
}
""")

ifftn = ({}, "",
"""template <typename T>
inline arma::Mat<typename T::elem_type> ifft(arma::cx_mat X, int n, int dim)
{
if (dim == 1)
X = arma::ifft(X, n) ;
else
X = arma::trans(arma::ifft(arma::trans(X)), n) ;
return X ;
}
""")
