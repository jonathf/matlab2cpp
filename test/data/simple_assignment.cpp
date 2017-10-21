#include <armadillo>
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
}

