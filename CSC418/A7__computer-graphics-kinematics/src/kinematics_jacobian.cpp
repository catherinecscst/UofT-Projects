#include "kinematics_jacobian.h"
#include "transformed_tips.h"
#include <iostream>

void kinematics_jacobian(
  const Skeleton & skeleton,
  const Eigen::VectorXi & b,
  Eigen::MatrixXd & J)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  J = Eigen::MatrixXd::Zero(b.size() * 3,skeleton.size() * 3);
  Eigen::VectorXd tips = transformed_tips(skeleton, b);
  double h = 1.0e-7;

  for (int i = 0; i < skeleton.size(); i++){
    for (int j = 0; j < skeleton[0].xzx.size(); j++){

      Skeleton copy_skeleton = skeleton;
      copy_skeleton[i].xzx[j] += h;
      
      Eigen::VectorXd dx_i = transformed_tips(copy_skeleton, b) - tips;
      for (int k = 0; k < J.rows(); k++){
        J(k, 3 * i + j) = dx_i[k] / h;
      }

    }
  }
  /////////////////////////////////////////////////////////////////////////////
}
