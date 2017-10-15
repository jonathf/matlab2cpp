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
