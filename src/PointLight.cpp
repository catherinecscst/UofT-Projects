#include "PointLight.h"

void PointLight::direction(
  const Eigen::Vector3d & q, Eigen::Vector3d & d, double & max_t) const
{
  // Compute the direction to a point light source and its parametric distance from a query point.

  d = (p - q).normalized();
  max_t = (p - q).norm();
  
}
