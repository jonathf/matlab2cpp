code = r"""#ifndef MCONVERT_H
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
        arma::uvec s;
        int n = b - a;
        if (n < 0) return s;
        s.set_size(n + 1);
        for (int ii = 0; ii <= n; ii++)
            s(ii) = ii + a;
        return s;
    }

    template <typename T>
    inline T span(int a, int b) {
        T s;
        int n = b - a;
        if (n < 0) return s;
        s.set_size(n + 1);
        for (int ii = 0; ii <= n; ii++)
            s(ii) = ii + a;
        return s;
    }

    inline arma::uvec span(int a, int step, int b)
    {
        arma::uvec s;
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
    inline arma::cx_mat fft(arma::Mat<typename T::elem_type> X, int dim)
    {
        if (dim == 1)
            return arma::fft(X);
        else
            return arma::strans(arma::fft(arma::strans(X)));

    }

    template <typename T>
    inline arma::cx_mat fft(arma::Mat<typename T::elem_type> X, int n, int dim)
    {
        if (dim == 1)
            return arma::fft(X, n);
        else
            return arma::strans(arma::fft(arma::strans(X), n));

    }


    inline arma::cx_mat ifft(arma::cx_mat X, int dim)
    {
        if (dim == 1)
            X = arma::ifft(X);
        else
            X = arma::strans(arma::ifft(arma::strans(X)));
        return X;
    }

    inline arma::cx_mat ifft(arma::cx_mat X, int n, int dim)
    {
        if (dim == 1)
            X = arma::ifft(X, n);
        else
            X = arma::strans(arma::ifft(arma::strans(X), n));
        return X;
    }
    

    //template<typename eT>
    inline rowvec fspan(double a, double step, double b) {
        //arma::Col<eT> s;
        rowvec s;
        int n = (int) ((b - a) / step);
        if (n < 0) return s;

        //s.set_size(n + 1);
        s.set_size(n+1);
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

    template<typename T1>
    inline T1 square(T1 a) {
        return a*a;
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

    /*
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
    */

    template<typename T>
    inline arma::Mat <typename T::elem_type> convmtx(const T& v, int m) {

        arma::Mat<typename T::elem_type> out = zeros<arma::Mat<typename T::elem_type> >(v.n_elem + m - 1, m);
        arma::Col<typename T::elem_type> aux((typename T::elem_type*)v.memptr(), v.n_elem);

        if (v.n_rows == 1)
        {
            for (int ii = 0; ii < m; ii++) {
                out.submat(ii, ii, ii + v.n_elem - 1, ii) = aux;
            }
        }
        else
        {
            for (int ii = 0; ii < m; ii++) {
                out.submat(ii, ii, ii + v.n_elem - 1, ii) = v;
            }
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

    template <typename eT>
    inline eT fix(const eT a) {
       return a > eT(0) ? floor(a) : ceil(a);
    }

    template<typename T>
    inline void intersect(arma::Col<typename T::elem_type>& C, arma::uvec& ia, arma::uvec& ib, const T& a, const T& b) {

       typedef typename eT T::elem_type;

       arma::uvec sa = arma::sort_index(a);
       arma::uvec sb = arma::sort_index(b);

       std::vector<eT> C_;
       std::vector<arma::uword> ia_, ib_;

       int na = int(a.n_elem);
       int nb = int(b.n_elem);
       int ja = 0, jb = 0;

       for (;;) {

          arma::uword sja = sa(ja);
          arma::uword sjb = sb(jb);

          eT ca = a(sja);
          eT cb = b(sjb);

          if (ca > cb) {
             ja++;
          }
          else if (cb > ca) {
             jb++;
          }
          else {
             C_.push_back(ca);
             ia_.push_back(sja);
             ib_.push_back(sjb);
             while (++ja < na && a(sa(ja)) == ca) {}
             while (++jb < nb && b(sb(jb)) == cb) {}
             if (ja == na || jb == nb)
                break;
          }

       }

       ia = arma::uvec(ia_) + 1;
       ib = arma::uvec(ib_) + 1;
       C = arma::Col<eT>(C_);
    }

    template<typename T>
    inline void intersect(arma::Col<typename T::elem_type>& C, const T& a, const T& b) {
       arma::uvec dum0, dum1;
       intersect(C, dum0, dum1, a, b);
    }

    template<typename Tr, typename T>
    inline void unique_rows_core(Tr& C, Tr& a_sorted, arma::uvec& ia, const T& a) {

       typedef typename T::elem_type eT;

       int ic_cur = 0;

       auto cmp = [&a, &ic_cur](const int k, const int l) -> bool {
          return a(k, ic_cur) < a(l, ic_cur);
       };

       int nr = int(a.n_rows);
       int nc = int(a.n_cols);

       arma::Col<eT> ac0(const_cast<eT*>(a.colptr(0)), nr, false);
       arma::uvec ord = arma::sort_index(a.col(0));
       std::vector<arma::uword> ia0, ia1;

       std::vector<arma::uword>* ia_ = &ia0;
       std::vector<arma::uword>* ia_prev_ = &ia1;

       ia_->push_back(0);
       for (int ii = 1; ii < nr; ii++) {
          if (a(ord(ii), 0) != a(ord(ii - 1))) {
             ia_->push_back(ii);
          }
       }
       ia_->push_back(nr);

       for (int ic = 1; ic < nc; ic++) {

          ic_cur = ic;
          int ir = 0, ir_prev = 0;
          std::swap(ia_prev_, ia_);
          int na = int(ia_prev_->size());
          ia_->clear();

          for (int ii = 0; ii < na - 1; ii++) {
             ia_->push_back((*ia_prev_)[ii]);
             int l = (*ia_prev_)[ii], u = (*ia_prev_)[ii + 1];
             std::sort(&ord(l), &(ord(u - 1)) + 1, cmp);
             for (int jj = l + 1; jj < u; jj++) {
                if (a(ord(jj - 1), ic) != a(ord(jj), ic)) {
                   ia_->push_back(jj);
                }
             }
          }

          ia_->push_back(nr);

       }

       ia = arma::uvec(*ia_);
       int na = int(ia.n_elem);
       C.set_size(na - 1, a.n_cols);

       for (int ii = 0; ii < na - 1; ii++) {
          C.row(ii) = a.row(ord(ia(ii)));
       }

       a_sorted.set_size(nr, nc);
       for (int ir = 0; ir < nr; ir++) {
          a_sorted.row(ir) = a.row(ord(ir));
       }
    }

    template<typename T>
    inline T sortrows(const T& a) {

       typedef typename T::elem_type eT;
       arma::uvec dum0;
       arma::Mat<eT> dum1;
       arma::Mat<eT> ret;
       unique_rows_core(dum1, ret, dum0, a);
       return ret;
    }

    template<typename T>
    inline void unique_rows(T& C, const T& a) {

       arma::uvec dum;
       unique_rows(C, dum, a);

    }

    template<typename T>
    inline T unique_rows(const T& a) {
       T ret;
       unique_rows(ret, a);
       return ret;
    }

    template<typename T>
    inline int isempty(const T& a) {
        return a.n_elem == 0;
    }

    template<typename T>
    inline void unique(T& a, const T& b, const char* m) {
        T tmp;
        const T& in = b;
        if (&a == &b) {
           tmp = b;
           in = tmp;
        }

        if (strcmp(m, "rows") == 0) {
           unique_rows(a, tmp);
        }
        else {
           fprintf(stderr, "m2pp::unique(): Unrecognized option %s\n", m);
        }
    }

    static arma::wall_clock timer_;

    inline double tic() {
       timer_.tic();
       return timer_.toc();
    }

    inline double toc() {
       return timer_.toc();
    }

    inline double toc(double start) {
       return timer_.toc() - start;
    }
}


#endif


"""
