#include "transformed_tips.h"
#include "forward_kinematics.h"

Eigen::VectorXd transformed_tips(
  const Skeleton & skeleton, 
  const Eigen::VectorXi & b)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  Eigen::VectorXd tips = Eigen::VectorXd::Zero(3 * b.size());
  std::vector<Eigen::Affine3d,Eigen::aligned_allocator<Eigen::Affine3d>> T;
  forward_kinematics(skeleton, T);

  for (int i = 0; i < b.size(); i++){

	Eigen::Vector4d tip = T[b[i]] * skeleton[b[i]].rest_T * Eigen::Vector4d(skeleton[b[i]].length, 0, 0, 1);
	tips[i * 3] = tip[0];
	tips[i * 3 + 1] = tip[1];
	tips[i * 3 + 2] = tip[2];

  }

  return tips;
  /////////////////////////////////////////////////////////////////////////////
}
