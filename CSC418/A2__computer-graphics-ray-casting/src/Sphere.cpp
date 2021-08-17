#include "Sphere.h"
#include "Ray.h"
#include <math.h>
bool Sphere::intersect(
  const Ray & ray, const double min_t, double & t, Eigen::Vector3d & n) const
{
  
  // Intersect a sphere with a ray.
  
  Eigen::Vector3d d = ray.direction;
  Eigen::Vector3d e = ray.origin;

  double discriminant = pow(d.dot(e - center), 2) - d.dot(d) * ((e - center).dot(e - center) - pow(radius, 2));

  if (discriminant == 0.0){
    double minimum = -d.dot(e - center) / d.dot(d);
    if (minimum > min_t){
      t = minimum;
      n = (e + t * d - center) / radius;
      return true;
    }
  }
  else if (discriminant > 0.0){

  	double minimum = (-d.dot(e - center) - std::sqrt(discriminant))/d.dot(d);
  	double maximum = (-d.dot(e - center) + std::sqrt(discriminant))/d.dot(d);

    if (minimum > min_t){
      t = minimum;
      n = (e + t * d - center) / radius;
      return true;
    }
    else if (minimum < min_t && maximum > min_t){
      t = maximum;
      n = (e + t * d - center) / radius;
      return true;
    }
  }

  return false;

}

