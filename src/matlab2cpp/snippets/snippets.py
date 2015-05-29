complex = ({}, """#include <complex>
#include <cmath>""", "")

armadillo = ({}, """#include <armadillo>
using namespace arma ;""", "")

# depricated (I think)
span = ({"target":"ivec", "start":"int","end":"int"},
"""inline %(target)s span( %(start)s start, int step, %(end)s end)
{
int numElem = int(end > start ? end - start : start - end) + 1;
%(target)s res((numElem + std::abs(step) - 1) / std::abs(step));
eT* pRes = res.memptr();
if (end > start)
{
assert(step > 0);
for (eT c = start; c <= end; c += step) *(pRes++) = c;
}
else
{
assert(end == start || step < 0);
for (eT c = end; c >= start; c -= step) *(pRes++) = c;
}
return res;
}""")

# from matrix to matrix
get_mm = ({"target":"fmat", "source":"fmat"},
"""inline %(target)s get_mm(const %(source)s& M, const int firstRow, const int stepRow, const int lastRow, const int firstCol, const int stepCol, const int lastCol)
{
%(target)s R;
int n = abs(lastRow-firstRow)/abs(stepRow) + 1;
int m = abs(lastCol-firstCol)/abs(stepCol) + 1;
R.set_size(n,m);
int i_step = 1;
int i_start = 0;
int j_step = 1;
int j_start = 0;
int i_src = firstRow;
int i = i_start;
while ( (stepRow>=0 && i_src>=firstRow && i_src<=lastRow) || (stepRow<0 && i_src<=firstRow && i_src>=lastRow) )
{
int j_src = firstCol;
int j = j_start;
while ( (stepCol>=0 && j_src>=firstCol && j_src<=lastCol) || (stepCol<0 && j_src<=firstCol && j_src>=lastCol) )
{
R(i,j) = M(i_src,j_src);
j+=j_step;
j_src+=stepCol;
}
i+=i_step;
i_src+=stepRow;
}
return R;
}""")

# from matrix to column vector
get_mc = ({"target":"fvec", "source":"fmat"},
"""inline %(target)s get_mc(const %(source)s& M, const int firstRow, const int stepRow, const int lastRow, const int col)
{
%(target)s R;
int n = abs(lastRow-firstRow)/abs(stepRow) + 1;
R.set_size(n,1);
int i_step = 1;
int i_start = 0;
int i_src = firstRow;
int i = i_start;
while ( (stepRow>=0 && i_src>=firstRow && i_src<=lastRow) || (stepRow<0 && i_src<=firstRow && i_src>=lastRow) )
{
R(i, 0) = M(i_src, col);
i+=i_step;
i_src+=stepRow;
}
return R;
}""")

# from matrix to row vector
get_mr = ({"target":"frowvec", "source":"fmat"},
"""inline %(target)s get_mr(const %(source)s& M, const int row, const int firstCol, const int stepCol, const int lastCol)
{
%(target)s R;
int m = abs(lastCol-firstCol)/abs(stepCol) + 1;
R.set_size(1,m);
int j_step = 1;
int j_start = 0;
int j_src = firstCol;
int j = j_start;
while ( (stepCol>=0 && j_src>=firstCol && j_src<=lastCol) || (stepCol<0 && j_src<=firstCol && j_src>=lastCol) )
{
R(0,j) = M(row, j_src);
j+=j_step;
j_src+=stepCol;
}
return R;
}""")


set_mm = ({"target":"fmat", "source":"fmat"},
"""inline void set_mm(%(target)s& R,const %(source)s& M, const int firstRow, const int stepRow, const int lastRow, const int firstCol, const int stepCol, const int lastCol)
{
int i_step = 1;
int i_start = 0;
int j_step = 1;
int j_start = 0;
int i_src = firstRow;
int i = i_start;
while ( (stepRow>=0 && i_src>=firstRow && i_src<=lastRow) || (stepRow<0 && i_src<=firstRow && i_src>=lastRow) )
{
int j_src = firstCol;
int j = j_start;
while ( (stepCol>=0 && j_src>=firstCol && j_src<=lastCol) || (stepCol<0 && j_src<=firstCol && j_src>=lastCol) )
{
R(i_src,j_src) = M(i,j);
j+=j_step;
j_src+=stepCol;
}
i+=i_step;
i_src+=stepRow;
}
return ;
}""")

set_mc = ({"target":"fmat", "source":"fmat"},
"""inline void set_mc(%(target)s& R,const %(source)s& M, const int firstRow, const int stepRow, const int lastRow, const int col)
{
int i_step = 1;
int i_start = 0;
int i_src = firstRow;
int i = i_start;
while ( (stepRow>=0 && i_src>=firstRow && i_src<=lastRow) || (stepRow<0 && i_src<=firstRow && i_src>=lastRow) )
{
R(i_src, col) = M(i, 0);
i+=i_step;
i_src+=stepRow;
}
return ;
}""")

set_mr = ({"target":"fmat", "source":"fmat"},
"""inline void set_mr(%(target)s& R,const %(source)s& M, const int row, const int firstCol, const int stepCol, const int lastCol)
{
int j_step = 1;
int j_start = 0;
int j_src = firstCol;
int j = j_start;
while ( (stepCol>=0 && j_src>=firstCol && j_src<=lastCol) || (stepCol<0 && j_src<=firstCol && j_src>=lastCol) )
{
R(row, j_src) = M(0, j);
j+=j_step;
j_src+=stepCol;
}
return ;
}""")
