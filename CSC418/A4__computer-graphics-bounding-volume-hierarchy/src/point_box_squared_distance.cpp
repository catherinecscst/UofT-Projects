#include "point_box_squared_distance.h"

double point_box_squared_distance(
  const Eigen::RowVector3d & query,
  const BoundingBox & box)
{
  
  // Compute the squared distance between a query point and a box
  
  double x = std::fmax(std::fmax(box.min_corner[0] - query[0], 0), (query[0] - box.max_corner[0]));
  double y = std::fmax(std::fmax(box.min_corner[1] - query[1], 0), (query[1] - box.max_corner[1]));
  double z = std::fmax(std::fmax(box.min_corner[2] - query[2], 0), (query[2] - box.max_corner[2]));
  return (x * x) + (y * y) + (z * z);

}
