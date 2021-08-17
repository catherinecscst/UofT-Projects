#include "blinn_phong_shading.h"
// Hint:
#include "first_hit.h"
#include <iostream>

Eigen::Vector3d blinn_phong_shading(
  const Ray & ray,
  const int & hit_id, 
  const double & t,
  const Eigen::Vector3d & n,
  const std::vector< std::shared_ptr<Object> > & objects,
  const std::vector<std::shared_ptr<Light> > & lights)
{
  
  // Compute the lit color of a hit object in the scene using Blinn-Phong shading model. 
  // This function should also shoot an additional ray to each light source to check for shadows.

  Eigen::Vector3d rgb(0, 0, 0);
  Eigen::Vector3d p = ray.origin + t * ray.direction;
  for (int i = 0; i < lights.size(); i++){
    double max_t;
    Eigen::Vector3d lr_dir;
    Ray light_ray;
    lights[i]->direction(p, lr_dir, max_t);
    light_ray.origin = p;
    light_ray.direction = lr_dir;

    int light_hit_id;
    double light_t;
    Eigen::Vector3d light_n;
    if (!first_hit(light_ray, 0.0000001, objects, light_hit_id, light_t, light_n) || light_t >= max_t){
      Eigen::Vector3d rdir_n = -ray.direction.normalized();
      Eigen::Vector3d lr_dir_n = lr_dir.normalized();
      Eigen::Vector3d h = (rdir_n + lr_dir_n).normalized();
      rgb += (objects[hit_id]->material->kd.array() * lights[i]->I.array()).matrix()
                                                    * fmax(0.0, n.dot(lr_dir));
      rgb += (objects[hit_id]->material->ks.array() * lights[i]->I.array()).matrix() 
                                                    * pow(fmax(0.0, n.dot(h)), objects[hit_id]->material->phong_exponent);
    }
  }
  rgb += (objects[hit_id]->material->ka.array() * Eigen::Vector3d(0.1, 0.1, 0.1).array()).matrix();

  return rgb;
  
}
