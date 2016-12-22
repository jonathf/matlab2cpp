import matlab2cpp
import tempfile
import os
import shutil
from shutil import copy

from subprocess import Popen, PIPE


def setup_module(module):
    """Create temporary folder and save path to module before start
    """
    module.path = tempfile.mkdtemp()
    module.curdir = os.path.abspath(os.path.curdir)

def teardown_module(module):
    """Remove temporary folder after job is complete
    """

    shutil.rmtree(module.path)


def test_variable_suggest():
    """Test basic variable types
    """

    # change to temporary dir
    os.chdir(path)

    m_code = """
a = 1
b = 2.
c = '3'
d = [4, 5]
e = [6; 7]
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("m2cpp test.m -rs > /dev/null")

    f = open("test.m.cpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n".join(converted_code.split("\n")[2:])

    reference_code = """#include <armadillo>
using namespace arma ;

int main(int argc, char** argv)
{
  double b ;
  int a ;
  irowvec d ;
  ivec e ;
  std::string c ;
  a = 1 ;
  b = 2. ;
  c = "3" ;
  sword _d [] = {4, 5} ;
  d = irowvec(_d, 2, false) ;
  sword _e [] = {6, 7} ;
  e = ivec(_e, 2, false) ;
  return 0 ;
}"""

    assert converted_code == reference_code



def test_function_suggestion():
    """Test suggestion for function with single return
    """

    # change to temporary dir
    os.chdir(path)

    m_code = """
function y=f(x)
    y = x+2
end
function g()
    x = [1,2,3]
    y = f(x)
end
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("m2cpp test.m -rs > /dev/null")

    f = open("test.m.hpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n".join(converted_code.split("\n")[2:])

    reference_code = """#ifndef F_M_HPP
#define F_M_HPP

#include <armadillo>
using namespace arma ;

irowvec f(irowvec x) ;
void g() ;

irowvec f(irowvec x)
{
  irowvec y ;
  y = x+2 ;
  return y ;
}

void g()
{
  irowvec x, y ;
  sword _x [] = {1, 2, 3} ;
  x = irowvec(_x, 3, false) ;
  y = f(x) ;
}
#endif"""

    assert converted_code == reference_code



def test_functions_suggestion():
    """Test suggestion for function with multiple returns
    """

    # change to temporary dir
    os.chdir(path)

    m_code = """
function [y,z]=f(a,b)
    y = a+2
    z = b-3
end
function g()
    a = [1,2,3]
    b = [4;5;6]
    [y,z] = f(a,b)
end
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("m2cpp test.m -rs > /dev/null")

    f = open("test.m.hpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n".join(converted_code.split("\n")[2:])

    reference_code = """#ifndef F_M_HPP
#define F_M_HPP

#include <armadillo>
using namespace arma ;

void f(irowvec a, ivec b, irowvec& y, ivec& z) ;
void g() ;

void f(irowvec a, ivec b, irowvec& y, ivec& z)
{
  y = a+2 ;
  z = b-3 ;
}

void g()
{
  irowvec a, y ;
  ivec b, z ;
  sword _a [] = {1, 2, 3} ;
  a = irowvec(_a, 3, false) ;
  sword _b [] = {4, 5, 6} ;
  b = ivec(_b, 3, false) ;
  f(a, b, y, z) ;
}
#endif"""

    assert reference_code == converted_code




def test_fx_decon():

    os.chdir(path)

    m_code = """
function [DATA_f] = fx_decon(DATA,dt,lf,mu,flow,fhigh);
 [nt,ntraces] = size(DATA);
 nf = 2^nextpow2(nt);
 DATA_FX_f = zeros(nf,ntraces);
 DATA_FX_b = zeros(nf,ntraces);
 ilow  = floor(flow*dt*nf)+1; 
  if ilow<1; 
   ilow=1; 
  end;
 ihigh = floor(fhigh*dt*nf)+1;
  if ihigh > floor(nf/2)+1; 
   ihigh=floor(nf/2)+1; 
  end
 DATA_FX = fft(DATA,nf,1);
 for k = ilow:ihigh;
  aux_in  = DATA_FX(k,:)';
  [aux_out_f,aux_out_b] = ar_modeling(aux_in,lf,mu);
  DATA_FX_f(k,:) = aux_out_f';
  DATA_FX_b(k,:) = aux_out_b';
 end;
 for k=nf/2+2:nf
  DATA_FX_f(k,:) = conj(DATA_FX_f(nf-k+2,:));
  DATA_FX_b(k,:) = conj(DATA_FX_b(nf-k+2,:));
 end
 DATA_f = real(ifft(DATA_FX_f,[],1));
 DATA_f = DATA_f(1:nt,:);
 DATA_b = real(ifft(DATA_FX_b,[],1));
 DATA_b = DATA_b(1:nt,:);
 DATA_f = (DATA_f + DATA_b);
 DATA_f(:,lf+1:ntraces-lf)= DATA_f(:,lf+1:ntraces-lf)/2;
return
function [yf,yb] = ar_modeling(x,lf,mu);
   nx = length(x);
   y  = x(1:nx-lf,1);
   C  = x(2:nx-lf+1,1);
   R  = x(nx-lf+1:nx,1);
   M = hankel(C,R);
   B = M'*M;  beta = B(1,1)*mu/100;
   ab = (B + beta*eye(lf))\M'*y;
   temp = M*ab;
   temp = [temp;zeros(lf,1)];
   yb = temp;
   y  = x(lf+1:nx,1);
   C  = x(lf:nx-1,1);
   R = flipud(x(1:lf,1));
   M = toeplitz(C,R);
   B = M'*M;  beta = B(1,1)*mu/100;
   af = (B + beta*eye(lf))\M'*y;
   temp = M*af;
   temp = [zeros(lf,1);temp];
   yf = temp;
return
    """

    py_file = """
functions = {
  "ar_modeling" : {
       "B" : "cx_mat",
       "C" : "cx_vec",
       "M" : "cx_mat",
       "R" : "cx_vec",
      "ab" : "cx_vec",
      "af" : "cx_vec",
    "beta" : "cx_double",
      "lf" : "int",
      "mu" : "double",
      "nx" : "uword",
    "temp" : "cx_mat",
       "x" : "cx_vec",
       "y" : "cx_vec",
      "yb" : "cx_vec",
      "yf" : "cx_vec",
  },
  "fx_decon" : {
         "DATA" : "mat",
      "DATA_FX" : "cx_mat",
    "DATA_FX_b" : "cx_mat",
    "DATA_FX_f" : "cx_mat",
       "DATA_b" : "mat",
       "DATA_f" : "mat",
       "aux_in" : "cx_vec",
    "aux_out_b" : "cx_vec",
    "aux_out_f" : "cx_vec",
           "dt" : "double",
        "fhigh" : "int",
         "flow" : "double",
        "ihigh" : "int",
         "ilow" : "int",
            "k" : "int",
           "lf" : "int",
           "mu" : "double",
           "nf" : "int",
           "nt" : "int",
      "ntraces" : "int",
  },
}
includes = [
  '#include <armadillo>',
  'using namespace arma ;',
]
    """

    reference_code = """
#ifndef FX_DECON_M_HPP
#define FX_DECON_M_HPP

#include <armadillo>
#include "mconvert.h"
#include <cmath>
using namespace arma ;

mat fx_decon(mat DATA, double dt, int lf, double mu, double flow, int fhigh) ;
void ar_modeling(cx_vec x, int lf, double mu, cx_vec& yf, cx_vec& yb) ;

mat fx_decon(mat DATA, double dt, int lf, double mu, double flow, int fhigh)
{
  cx_mat DATA_FX, DATA_FX_b, DATA_FX_f ;
  cx_vec aux_in, aux_out_b, aux_out_f ;
  int ihigh, ilow, k, nf, nt, ntraces ;
  mat DATA_b, DATA_f ;
  nt = DATA.n_rows ;
  ntraces = DATA.n_cols ;
  nf = pow(2, m2cpp::nextpow2(nt)) ;
  DATA_FX_f = arma::zeros<cx_mat>(nf, ntraces) ;
  DATA_FX_b = arma::zeros<cx_mat>(nf, ntraces) ;
  ilow = std::floor(flow*dt*nf)+1 ;
  if (ilow<1)
  {
    ilow = 1 ;
  }
  ihigh = std::floor(fhigh*dt*nf)+1 ;
  if (ihigh>std::floor(nf/2.0)+1)
  {
    ihigh = std::floor(nf/2.0)+1 ;
  }
  DATA_FX = m2cpp::fft<mat>(DATA, nf, 1) ;
  for (k=ilow; k<=ihigh; k++)
  {
    aux_in = arma::trans(DATA_FX.row(k-1)) ;
    ar_modeling(aux_in, lf, mu, aux_out_f, aux_out_b) ;
    DATA_FX_f.row(k-1) = arma::trans(aux_out_f) ;
    DATA_FX_b.row(k-1) = arma::trans(aux_out_b) ;
  }
  for (k=nf/2.0+2; k<=nf; k++)
  {
    DATA_FX_f.row(k-1) = arma::conj(DATA_FX_f.row(nf-k+1)) ;
    DATA_FX_b.row(k-1) = arma::conj(DATA_FX_b.row(nf-k+1)) ;
  }
  DATA_f = arma::real(m2cpp::ifft<cx_mat>(DATA_FX_f, 1)) ;
  DATA_f = DATA_f.rows(arma::span(0, nt-1)) ;
  DATA_b = arma::real(m2cpp::ifft<cx_mat>(DATA_FX_b, 1)) ;
  DATA_b = DATA_b.rows(arma::span(0, nt-1)) ;
  DATA_f = (DATA_f+DATA_b) ;
  DATA_f.cols(arma::span(lf, ntraces-lf-1)) = DATA_f.cols(arma::span(lf, ntraces-lf-1))/2.0 ;
  return DATA_f ;
}

void ar_modeling(cx_vec x, int lf, double mu, cx_vec& yf, cx_vec& yb)
{
  cx_double beta ;
  cx_mat B, M, temp ;
  cx_vec C, R, ab, af, y ;
  uword nx ;
  nx = m2cpp::length(x) ;
  y = x(arma::span(0, nx-lf-1)) ;
  C = x(arma::span(1, nx-lf)) ;
  R = x(arma::span(nx-lf, nx-1)) ;
  M = m2cpp::hankel(C, R) ;
  B = arma::trans(M)*M ;
  beta = B(0, 0)*mu/100.0 ;
  ab = arma::solve((B+beta*arma::eye<cx_mat>(lf, lf)), arma::trans(M), solve_opts::fast)*y ;
  temp = M*ab ;
  temp = arma::join_cols(temp, arma::zeros<cx_mat>(lf, 1)) ;
  yb = temp ;
  y = x(arma::span(lf, nx-1)) ;
  C = x(arma::span(lf-1, nx-2)) ;
  R = arma::flipud(x(arma::span(0, lf-1))) ;
  M = toeplitz(C, R) ;
  B = arma::trans(M)*M ;
  beta = B(0, 0)*mu/100.0 ;
  af = arma::solve((B+beta*arma::eye<cx_mat>(lf, lf)), arma::trans(M), solve_opts::fast)*y ;
  temp = M*af ;
  temp = arma::join_cols(arma::zeros<cx_mat>(lf, 1), temp) ;
  yf = temp ;
  return ;
}
#endif
    """

    f = open("fx_decon.m", "w")
    f.write(m_code)
    f.close()

    f = open("fx_decon.m.py", "w")
    f.write(py_file)
    f.close()

    os.system("m2cpp fx_decon.m -s > /dev/null")

    f = open("fx_decon.m.hpp", "r")
    converted_code = "\n".join(f.read().split("\n")[2:]).strip()
    f.close()

    reference_code = reference_code.strip()

    assert converted_code == reference_code



if __name__ == "__main__":
    os.system("py.test --tb short")
