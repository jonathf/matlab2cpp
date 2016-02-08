code = """#ifndef MCONVERT_H
#define MCONVERT_H

#include <armadillo>
using namespace arma;

namespace m2cpp {

	
  template<typename eT> 
  inline arma::Col<eT> scol(eT a) {
    return arma::Col<eT>(&a, 1, true);
  }

  template<typename eT>
  inline arma::Row<eT> srow(eT a) {
    return arma::Row<eT>(&a, 1, true);
  }

  template<typename eT>
  inline arma::Mat<eT> smat(eT a) {
    return arma::Mat<eT>(&a, 1, 1, true);
  }


  inline arma::uvec span(int a, int b) {
	  arma::uvec s((arma::uword)0);
	  int n = b - a;
	  if (n < 0) return s;
	  s.set_size(n + 1);
	  for (int ii = 0; ii <= n; ii++)
		  s(ii) = ii + a;
	  return s;
  }

  template <typename T>
  inline T span(int a, int b) {
	  T s((arma::uword)0);
	  int n = b - a;
	  if (n < 0) return s;
	  s.set_size(n + 1);
	  for (int ii = 0; ii <= n; ii++)
		  s(ii) = ii + a;
	  return s;
  }


  template <typename T>
  inline T span(int a, int step, int b)
  {
	  T s;
	  int n = (b - a + step) / step;
	  if (n < 0)
	  {
		  return s;
	  }
	  s.set_size(n);

	  for (int ii = 0; ii < n; ii++)
	  {
		  s(ii) = step * ii + a;
	  }

	  return s;
   }
  


   template <typename T>
   inline arma::cx_mat fft(arma::Mat<typename T::elem_type> X, int n, int dim)
   {
	   if (dim == 1)
		   return arma::fft(X, n);
	   else
		   return arma::strans(arma::fft(arma::strans(X), n));

   }


	template <typename T>
	inline arma::Mat<typename T::elem_type> ifft(arma::cx_mat X, int dim)
	{
		if (dim == 1)
			X = arma::ifft(X);
		else
			X = arma::strans(arma::ifft(arma::strans(X)));
		return X;
	}


   template<typename eT>
   inline typename arma::enable_if2<arma::is_real<eT>::value, arma::Col<eT> >::result fspan(eT a, eT step, eT b) {
      arma::Col<eT> s;
      int n = int((b - a) / step);
      if (n < 0) return s;

      s.set_size(n + 1);
      for (int ii = 0; ii <= n; ii++)
        s(ii) = step * ii + a;
      return s;
  }


  inline int nextpow2(int n) {
    n = abs(n);
    int p = 0;
    int tmp = 1;
    while (tmp < n)
	{
      tmp *= 2;
      p++;
    }
    return p;
  }


  template<typename T1, typename T2>
  inline  arma::Mat<typename T1::elem_type> hankel(const T1& c_, const T2& r_) {

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

  template<typename T>
  inline arma::Mat <typename T::elem_type> convmtx(const T& v, int m) {

	  arma::Mat<typename T::elem_type> out = zeros(v.n_elem + m - 1, m);
	  arma::Col<typename T::elem_type> aux((typename T::elem_type*)v.memptr(), v.n_elem);

	  for (int ii = 0; ii < m; ii++) {
		  out.submat(ii, ii, ii + v.n_elem - 1, ii) = v;
	  }

	  if (v.n_rows == 1)
		  out = out.t();
	  return out;
  }

  template <typename eT>
	  inline typename arma::enable_if2< arma::is_real<typename eT::elem_type>::value, typename arma::Mat<typename eT::elem_type> >::result
	  conv2(const arma::Mat<typename eT::elem_type>& A, const arma::Mat<typename eT::elem_type>& B) {
	  uword n = A.n_rows + B.n_rows - 1;
	  uword m = A.n_rows + B.n_rows - 1;

	  arma::Mat<typename eT::elem_type> out = arma::real(arma::ifft2(fft2(A, n, m) % fft2(B, n, m)));
	  return out;
  }

  template <typename eT, typename fT>
	  inline typename arma::enable_if2 < arma::is_complex<typename eT::elem_type>::value || arma::is_complex<typename fT::elem_type>::value,
	  arma::Mat<typename std::complex< typename arma::get_pod_type<eT>::result > > >::result
	  conv2(const arma::Mat<typename eT::elem_type>& A, const arma::Mat<typename fT::elem_type>& B) {
	  uword n = A.n_rows + B.n_rows - 1;
	  uword m = A.n_rows + B.n_rows - 1;

	  arma::Mat<typename eT::elem_type> out = arma::ifft2(fft2(A, n, m) % fft2(B, n, m));
	  return out;
  }


}


#endif
"""
