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
  nt = DATA.n_rows;
  ntraces = DATA.n_cols;
  
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
  beta = B(0, 0)*(cx_double) mu/100.0 ;
  ab = arma::solve((B+beta*arma::eye<cx_mat>(lf, lf)), arma::trans(M), solve_opts::fast)*y ;
  temp = M*ab ;
  temp = arma::join_cols(temp, arma::zeros<cx_mat>(lf, 1)) ;
  yb = temp ;
  y = x(arma::span(lf, nx-1)) ;
  C = x(arma::span(lf-1, nx-2)) ;
  R = arma::flipud(x(arma::span(0, lf-1))) ;
  M = toeplitz(C, R) ;
  B = arma::trans(M)*M ;
  beta = B(0, 0)*(cx_double) mu/100.0 ;
  af = arma::solve((B+beta*arma::eye<cx_mat>(lf, lf)), arma::trans(M), solve_opts::fast)*y ;
  temp = M*af ;
  temp = arma::join_cols(arma::zeros<cx_mat>(lf, 1), temp) ;
  yf = temp ;
  return ;
}
#endif
