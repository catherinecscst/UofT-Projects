#include "insert_box_into_box.h"

void insert_box_into_box(
  const BoundingBox & A,
  BoundingBox & B)
{
  
  // Grow a box B by inserting a box A.

  B.min_corner(0) = std::fmin(A.min_corner(0), B.min_corner(0));
  B.max_corner(0) = std::fmax(A.max_corner(0), B.max_corner(0));

  B.min_corner(1) = std::fmin(A.min_corner(1), B.min_corner(1));
  B.max_corner(1) = std::fmax(A.max_corner(1), B.max_corner(1));

  B.min_corner(2) = std::fmin(A.min_corner(2), B.min_corner(2));
  B.max_corner(2) = std::fmax(A.max_corner(2), B.max_corner(2));
}

