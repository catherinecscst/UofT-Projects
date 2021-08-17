#include "line_search.h"
#include <iostream>

double line_search(
  const std::function<double(const Eigen::VectorXd &)> & f,
  const std::function<void(Eigen::VectorXd &)> & proj_z,
  const Eigen::VectorXd & z,
  const Eigen::VectorXd & dz,
  const double max_step)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code

  double sigma = max_step;
  double E = f(z);
  Eigen::VectorXd move_z = z - sigma * dz;
  proj_z(move_z);

  while (f(move_z) > E) {
  	// decrease  by a constant factor
    sigma /= 2.0;
    move_z = z - sigma * dz;
    proj_z(move_z);
  }

  return sigma;

  /////////////////////////////////////////////////////////////////////////////
}
