#include "first_hit.h"
#include <iostream>
#include <limits>
bool first_hit(
  const Ray & ray, 
  const double min_t,
  const std::vector< std::shared_ptr<Object> > & objects,
  int & hit_id, 
  double & t,
  Eigen::Vector3d & n)
{
  
  //Find the first (visible) hit given a ray and a collection of scene objects

  double min_dist = std::numeric_limits<double>::infinity();
  Eigen::Vector3d min_norm;
  int hit = -1;

  for (int i = 0; i < objects.size(); i++){

    double dist;
    Eigen::Vector3d normal;

    if (objects[i]->intersect(ray, min_t, dist, normal)){
      if (dist < min_dist){
        hit = i;
        min_dist = dist;
        min_norm = normal;
      }
    }
  }

  if (hit > -1){
    hit_id = hit;
    t = min_dist;
    n = min_norm;
    return true;
  }

  return false;

}

