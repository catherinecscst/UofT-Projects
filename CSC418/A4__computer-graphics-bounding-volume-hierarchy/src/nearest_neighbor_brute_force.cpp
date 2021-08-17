#include "nearest_neighbor_brute_force.h"
#include <limits>// std::numeric_limits<double>::infinity();
#include <iostream>

void nearest_neighbor_brute_force(
  const Eigen::MatrixXd & points,
  const Eigen::RowVector3d & query,
  int & I,
  double & sqrD)
{
  
  // Compute the nearest neighbor for a query in the set of  points (rows of points). 
  // This should be a slow reference implementation. Aim for a computational complexity of but focus on correctness.
  
  I = -1;
  sqrD = std::numeric_limits<double>::infinity();

  for (int i = 0; i < points.rows(); i++){
    double d = (query-points.row(i)).squaredNorm();
    if (d < sqrD){
      I = i;
      sqrD = d;
    }
  }

}
