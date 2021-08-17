#include "euler_angles_to_transform.h"

Eigen::Affine3d euler_angles_to_transform(
  const Eigen::Vector3d & xzx)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  Eigen::Affine3d A;
  A.matrix() << 
    1, 0, 0, 0,
    0, cos(xzx[0] * M_PI/180.0), -sin(xzx[0] * M_PI/180.0), 0,
    0, sin(xzx[0] * M_PI/180.0), cos(xzx[0] * M_PI/180.0), 0,
    0, 0, 0, 1;
  Eigen::Affine3d B;
  B.matrix() << 
    cos(xzx[1] * M_PI/180.0), -sin(xzx[1] * M_PI/180.0), 0, 0,
    sin(xzx[1] * M_PI/180.0), cos(xzx[1] * M_PI/180.0), 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1;
  Eigen::Affine3d C;
  C.matrix() << 
    1, 0, 0, 0,
    0, cos(xzx[2] * M_PI/180.0), -sin(xzx[2] * M_PI/180.0), 0,
    0, sin(xzx[2] * M_PI/180.0), cos(xzx[2] * M_PI/180.0), 0,
    0, 0, 0, 1;
  return A * B * C;
  /////////////////////////////////////////////////////////////////////////////
}
