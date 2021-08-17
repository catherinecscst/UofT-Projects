#include "end_effectors_objective_and_gradient.h"
#include "transformed_tips.h"
#include "kinematics_jacobian.h"
#include "copy_skeleton_at.h"
#include <iostream>

void end_effectors_objective_and_gradient(
  const Skeleton & skeleton,
  const Eigen::VectorXi & b,
  const Eigen::VectorXd & xb0,
  std::function<double(const Eigen::VectorXd &)> & f,
  std::function<Eigen::VectorXd(const Eigen::VectorXd &)> & grad_f,
  std::function<void(Eigen::VectorXd &)> & proj_z)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  f = [&](const Eigen::VectorXd & A)->double
  {
    Skeleton copy_skeleton = copy_skeleton_at(skeleton, A);
    Eigen::VectorXd transformed = transformed_tips(copy_skeleton, b);
    // return 0.0;
    double r = 0.0;
    for (int i = 0; i < b.size(); i++){
      r += (Eigen::Vector3d(transformed[3 * i], transformed[3 * i + 1], transformed[3 * i + 2]) 
          - Eigen::Vector3d(xb0[3 * i], xb0[3 * i + 1], xb0[3 * i + 2])).squaredNorm();
    }
    return r;
  };

  grad_f = [&](const Eigen::VectorXd & A)->Eigen::VectorXd
  {

    Skeleton copy_skeleton = copy_skeleton_at(skeleton, A);
    Eigen::VectorXd transformed = transformed_tips(copy_skeleton, b);
    
    Eigen::MatrixXd J;
    kinematics_jacobian(copy_skeleton, b, J);

    // return Eigen::VectorXd::Zero(A.size());
    Eigen::VectorXd dE_dx = Eigen::VectorXd::Zero(3 * b.size());

    double E_pre = f(A);
    double dx = 1.0e-7;

    for (int i = 0; i < dE_dx.size(); i++){

      Eigen::VectorXd copy_transformed = transformed;
      copy_transformed[i] += dx;

      double r = 0.0;
      for (int j = 0; j < b.size(); j++){
        r += (Eigen::Vector3d(copy_transformed[3 * j], copy_transformed[3 * j + 1], copy_transformed[3 * j + 2]) 
            - Eigen::Vector3d(xb0[3 * j], xb0[3 * j + 1], xb0[3 * j + 2])).squaredNorm();
      }

      dE_dx[i] = (r - E_pre) / dx;

    }
    // J^T * dE/dx
    return J.transpose() * dE_dx;

  };
  proj_z = [&](Eigen::VectorXd & A)
  {
    for (int i = 0; i < skeleton.size(); i++) {
      A[3 * i] = std::max(skeleton[i].xzx_min[0], std::min(skeleton[i].xzx_max[0], A[3 * i]));
      A[3 * i + 1] = std::max(skeleton[i].xzx_min[1], std::min(skeleton[i].xzx_max[1], A[3 * i + 1]));
      A[3 * i + 2] = std::max(skeleton[i].xzx_min[2], std::min(skeleton[i].xzx_max[2], A[3 * i + 2]));
    }

    assert(skeleton.size() * 3 == A.size());
  
  };
  /////////////////////////////////////////////////////////////////////////////
}
