#include "triangle_area_normal.h"
#include <Eigen/Geometry>

Eigen::RowVector3d triangle_area_normal(
  const Eigen::RowVector3d & a, 
  const Eigen::RowVector3d & b, 
  const Eigen::RowVector3d & c)
{
  
  // Compute the normal vector of a 3D triangle given its corner locations. 
  // The output vector should have length equal to the area of the triangle.

  Eigen::RowVector3d n = -((c-a).cross(b-a)).normalized();
  double area =  ((c-a).cross(b-a)).norm() / 2.0;
  return area * n;

  // Eigen::RowVector3d n = ((b-a).cross(c-a)).normalized();
  // double area = ((b-a).cross(c-a)).norm() / 2.0;

}
