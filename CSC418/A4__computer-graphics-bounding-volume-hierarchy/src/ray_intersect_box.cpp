#include "ray_intersect_box.h"
#include <iostream>
#include <math.h>

bool ray_intersect_box(
  const Ray & ray,
  const BoundingBox& box,
  const double min_t,
  const double max_t)
{
  
  // Intersect a ray with a solid box 
  // (careful: if the ray or min_t lands inside the box this could still hit something stored inside the box, 
  //           so this counts as a hit).

  double xd = 1 / ray.direction(0);
  double yd = 1 / ray.direction(1);
  double zd = 1 / ray.direction(2);
  double tx_min,tx_max,ty_min,ty_max,tz_min,tz_max;
  double max_min, min_max;

  if (xd >= 0) {
    tx_min = xd * (box.min_corner(0) - ray.origin(0));
    tx_max = xd * (box.max_corner(0) - ray.origin(0));
  } 
  else{
    tx_min = xd * (box.max_corner(0) - ray.origin(0));
    tx_max = xd * (box.min_corner(0) - ray.origin(0));
  }

  if (yd >= 0) {
    ty_min = yd * (box.min_corner(1) - ray.origin(1));
    ty_max = yd * (box.max_corner(1) - ray.origin(1));
  } 
  else{
    ty_min = yd * (box.max_corner(1) - ray.origin(1));
    ty_max = yd * (box.min_corner(1) - ray.origin(1));
  }

  if (zd >= 0) {
    tz_min = zd * (box.min_corner(2) - ray.origin(2));
    tz_max = zd * (box.max_corner(2) - ray.origin(2));
  } 
  else{
    tz_min = zd * (box.max_corner(2) - ray.origin(2));
    tz_max = zd * (box.min_corner(2) - ray.origin(2));
  }

  max_min = std::fmax(std::fmax(tx_min, ty_min), tz_min);
  min_max = std::fmin(std::fmin(tx_max, ty_max), tz_max);

  if (min_max < max_min){
    return false;
  }

  if (std::fmin(max_t, min_max) < std::fmax(min_t, max_min)){
  	return false;
  }
  return true;

}
