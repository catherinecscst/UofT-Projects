#include "signed_incidence_matrix_dense.h"

void signed_incidence_matrix_dense(
  const int n,
  const Eigen::MatrixXi & E,
  Eigen::MatrixXd & A)
{
  //////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  A = Eigen::MatrixXd::Zero(E.rows(),n);

  int j, k; 	
  for (int i = 0; i < A.rows(); i++){
    j = E(i, 0);
	k = E(i, 1);
	A(i, j) = 1;
	A(i, k) = -1;
  }
  //////////////////////////////////////////////////////////////////////////////
}
