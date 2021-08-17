#include "fast_mass_springs_step_sparse.h"
#include <igl/matlab_format.h>

void fast_mass_springs_step_sparse(
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & E,
  const double k,
  const Eigen::VectorXi & b,
  const double delta_t,
  const Eigen::MatrixXd & fext,
  const Eigen::VectorXd & r,
  const Eigen::SparseMatrix<double>  & M,
  const Eigen::SparseMatrix<double>  & A,
  const Eigen::SparseMatrix<double>  & C,
  const Eigen::SimplicialLLT<Eigen::SparseMatrix<double> > & prefactorization,
  const Eigen::MatrixXd & Uprev,
  const Eigen::MatrixXd & Ucur,
  Eigen::MatrixXd & Unext)
{
  //////////////////////////////////////////////////////////////////////////////
  // Replace with your code

  Eigen::MatrixXd d = Eigen::MatrixXd::Zero(E.rows(),3);

  Eigen::MatrixXd y, l;
  Eigen::MatrixXd p = Ucur;
  
  Eigen::MatrixXd Cprest = Eigen::MatrixXd::Zero(b.size(),3);
  for (int i=0; i < Cprest.rows(); i++){
    Cprest.row(i) = V.row(b(i)); 
  }
  
  for(int iter = 0;iter < 50; iter++)
  {   
    for (int i = 0; i < d.rows(); i++){
      d.row(i) = r(i)* (p.row(E(i, 0)) - p.row(E(i, 1))).normalized();
    }
    y =  1 / (delta_t * delta_t) * M * (2 * Ucur - Uprev) + fext;

    double w = 1e10;  
    l = k * A.transpose() * d + y + w * C.transpose() * Cprest;

    p = prefactorization.solve(l);
  } 

  Unext = p;
  //////////////////////////////////////////////////////////////////////////////
}
