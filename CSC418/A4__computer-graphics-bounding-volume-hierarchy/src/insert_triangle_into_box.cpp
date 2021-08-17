#include "insert_triangle_into_box.h"

void insert_triangle_into_box(
  const Eigen::RowVector3d & a,
  const Eigen::RowVector3d & b,
  const Eigen::RowVector3d & c,
  BoundingBox & B)
{
  
  // Grow a box B by inserting a triangle with corners a, b, and c.

  B.min_corner(0) = std::fmin(std::fmin(a[0], b[0]), std::fmin(c[0], B.min_corner(0)));
  B.max_corner(0) = std::fmax(std::fmax(a[0], b[0]), std::fmax(c[0], B.max_corner(0)));

  B.min_corner(1) = std::fmin(std::fmin(a[1], b[1]), std::fmin(c[1], B.min_corner(1)));
  B.max_corner(1) = std::fmax(std::fmax(a[1], b[1]), std::fmax(c[1], B.max_corner(1)));

  B.min_corner(2) = std::fmin(std::fmin(a[2], b[2]), std::fmin(c[2], B.min_corner(2)));
  B.max_corner(2) = std::fmax(std::fmax(a[2], b[2]), std::fmax(c[2], B.max_corner(2)));
}


