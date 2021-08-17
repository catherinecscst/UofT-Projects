#include "Plane.h"
#include "Ray.h"

bool Plane::intersect(
  const Ray & ray, const double min_t, double & t, Eigen::Vector3d & n) const
{
  
  // Intersect a plane with a ray.
  
  Eigen::Vector3d d = ray.direction;
  Eigen::Vector3d e = ray.origin;

  if (d.dot(normal) != 0){
  	double t_out = (point - e).dot(normal) / d.dot(normal);
    if (t_out >= min_t){
	    t = t_out;
	    n = normal;
	    return true;
	  }
  }

  return false;

}

