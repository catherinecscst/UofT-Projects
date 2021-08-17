#include "DirectionalLight.h"
#include <limits>

void DirectionalLight::direction(
  const Eigen::Vector3d & q, Eigen::Vector3d & d, double & max_t) const
{
  
  // Compute the direction to a direction light source and its parametric distance from a query point (infinity).
  
  d = (-this->d).normalized();
  max_t = std::numeric_limits<double>::infinity();
  
}

