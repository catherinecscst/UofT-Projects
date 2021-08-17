#include <Eigen/Core>

Eigen::Vector3d reflect(const Eigen::Vector3d & in, const Eigen::Vector3d & n)
{

  // Given an "incoming" vector and a normal vector, compute the mirror reflected "outgoing" vector.
  return (in - 2 * (in.dot(n)) * n).normalized();
  
}
