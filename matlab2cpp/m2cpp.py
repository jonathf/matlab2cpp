code = """#ifndef MCONVERT_H
#define MCONVERT_H

#include <armadillo>


namespace m2cpp {

  
  template<typename eT> 
  inline 
  arma::Col<eT> 
  scol(const eT a) {
    return arma::Col<eT>(&a, 1, true);
  }

  template<typename eT>
  inline
  arma::Row<eT>
    srow(const eT a) {
    return arma::Row<eT>((eT*)&a, 1, true);
  }

  template<typename eT>
  inline
  arma::Mat<eT>
    smat(const eT a) {
    return arma::Mat<eT>(&a, 1, 1, true);
  }

  inline
  arma::uvec span(int a, int b) {
    arma::uvec s((arma::uword)0);
    int n = b - a;
    if (n < 0) return s;
    s.set_size(n + 1);
    for (int ii = 0; ii <= n; ii++)
      s(ii) = ii + a;
    return s;
  }

  inline
  arma::uvec span(int a, int step, int b) {
    arma::uvec s((arma::uword)0);
    int n = (b - a) / step;
    if (n < 0) return s;

    s.set_size(n + 1);
    for (int ii = 0; ii <= n; ii++)
      s(ii) = step * ii + a;
    return s;
  }

  
  template<typename eT>
  inline
  typename arma::enable_if2<arma::is_real<eT>::value, arma::Col<eT> >::result
    fspan(eT a, eT step, eT b) {
    arma::Col<eT> s;
    int n = int((b - a) / step);
    if (n < 0) return s;

    s.set_size(n + 1);
    for (int ii = 0; ii <= n; ii++)
      s(ii) = step * ii + a;
    return s;
  }


  inline
    int nextpow2(int n) {
    n = abs(n);
    int p = 0;
    int tmp = 1;
    while (tmp < n) {
      tmp *= 2;
      p++;
    }
    return p;
  }


  template<typename T1, typename T2>
  inline
    arma::Mat<typename T1::elem_type> hankel(const T1& c_, const T2& r_) {

	typedef typename T1::elem_type eT;

    int nc = r_.n_elem;
    int nr = c_.n_elem;

    const arma::Col<eT> c((eT*)c_.memptr(), nr, 0);
    const arma::Row<eT> r((eT*)r_.memptr(), nc, 0);

    if (r[0] != c[0]) {
      //("hankel: differing diagonal element. Using the column one");
    }

    arma::Mat<typename T1::elem_type> retval(nr, nc);

    for (int i = 1; i <= std::min(nr, nc); i++) {
      retval.submat(1 - 1, i - 1, nr - i + 1 - 1, i - 1) = c.rows(i - 1, nr
        - 1);
    }
    int tmp = 1;
    if (nc <= nr) {
      tmp = nr - nc + 2;
    }

    for (int i = nr; i >= tmp; i--) {
      retval.submat(i - 1, 2 + nr - i - 1, i - 1, nc - 1) = r.cols(2
        - 1, nc - nr + i - 1);
    }
    return retval;
  }

  template<typename T1>
  inline arma::uword length(const T1& A) {
    return A.n_elem;
  }

}


#endif"""
