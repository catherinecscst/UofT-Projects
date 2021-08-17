#include "TriangleSoup.h"
#include "Ray.h"
// Hint
#include "first_hit.h"

bool TriangleSoup::intersect(
  const Ray & ray, const double min_t, double & t, Eigen::Vector3d & n) const
{
  
  // Intersect a triangle soup with a ray.

  int i = 0; 
  
  return first_hit(ray, min_t, triangles, i, t, n);

}



