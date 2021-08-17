#include "fast_mass_springs_precomputation_sparse.h"
#include "signed_incidence_matrix_sparse.h"
#include <vector>

bool fast_mass_springs_precomputation_sparse(
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & E,
  const double k,
  const Eigen::VectorXd & m,
  const Eigen::VectorXi & b,
  const double delta_t,
  Eigen::VectorXd & r,
  Eigen::SparseMatrix<double>  & M,
  Eigen::SparseMatrix<double>  & A,
  Eigen::SparseMatrix<double>  & C,
  Eigen::SimplicialLLT<Eigen::SparseMatrix<double> > & prefactorization)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code

  std::vector<Eigen::Triplet<double> > ijv_m, ijv_c;

  const int n = V.rows();  
  Eigen::SparseMatrix<double> Q(n,n);

  r.resize(E.rows()); //r = Eigen::VectorXd::Zero(E.rows());
  M.resize(V.rows(),V.rows());
  C.resize(b.size(), V.rows()); 
  
  
  for (int i = 0; i < E.rows(); i++){
    r(i) = (V.row(E(i, 0)) - V.row(E(i, 1))).norm();
  }

  for (int i = 0; i < M.rows(); i++){
    ijv_m.emplace_back(i, i, m(i));
  }
  M.setFromTriplets(ijv_m.begin(), ijv_m.end());
  
  signed_incidence_matrix_sparse(V.rows(), E, A);
  
  for (int i=0; i < C.rows(); i++){
    ijv_c.emplace_back(i, b(i),1);
  }
  C.setFromTriplets(ijv_c.begin(), ijv_c.end());
  
  double w = 1e10;  
  Q = k * A.transpose() * A + (1 / (delta_t * delta_t) * M) + w * C.transpose() * C;

  /////////////////////////////////////////////////////////////////////////////
  prefactorization.compute(Q);
  return prefactorization.info() != Eigen::NumericalIssue;
}
