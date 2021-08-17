#include "forward_kinematics.h"
#include "euler_angles_to_transform.h"
#include <functional> // std::function



Eigen::Affine3d transformation_prev(const Skeleton & skeleton, int i){
  
  if (skeleton[i].parent_index == -1){
    return Eigen::Affine3d::Identity();
  } else {
  	Eigen::Affine3d parent = transformation_prev(skeleton, skeleton[i].parent_index);
    Eigen::Affine3d rest_T = skeleton[i].rest_T;
    return parent * rest_T * euler_angles_to_transform(skeleton[i].xzx) * rest_T.inverse();
  }
}

void forward_kinematics(
  const Skeleton & skeleton,
  std::vector<Eigen::Affine3d,Eigen::aligned_allocator<Eigen::Affine3d> > & T)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  T.resize(skeleton.size(),Eigen::Affine3d::Identity());

  for (int i = 1; i < skeleton.size(); i++){
    
    T[i] = transformation_prev(skeleton, i);
  
  }
  /////////////////////////////////////////////////////////////////////////////
}