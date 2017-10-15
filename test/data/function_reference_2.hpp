#ifndef F_M_HPP
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
#endif
