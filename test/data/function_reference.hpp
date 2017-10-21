#ifndef F_M_HPP
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
#endif
