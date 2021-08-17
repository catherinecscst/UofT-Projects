#include "raycolor.h"
#include "first_hit.h"
#include "blinn_phong_shading.h"
#include "reflect.h"

bool raycolor(
  const Ray & ray, 
  const double min_t,
  const std::vector< std::shared_ptr<Object> > & objects,
  const std::vector< std::shared_ptr<Light> > & lights,
  const int num_recursive_calls,
  Eigen::Vector3d & rgb)
{
  
  // Make use of first_hit.cpp to shoot a ray into the scene, collect hit information and use this to return a color value.
  
  if (num_recursive_calls > 5){
    return false;
  }

  int hit_id;
  double t;
  Eigen::Vector3d normal;
  rgb = Eigen::Vector3d(0,0,0);

  if (first_hit(ray, min_t, objects, hit_id, t, normal)){
    Ray reflect_ray;
    reflect_ray.origin = ray.origin + (ray.direction * t);
    reflect_ray.direction = reflect(ray.direction.normalized(), normal);
    rgb += blinn_phong_shading(ray, hit_id, t, normal, objects, lights);
    Eigen::Vector3d rgb_n;
    if (raycolor(reflect_ray, 0.0000001, objects, lights, num_recursive_calls + 1, rgb_n)){
      rgb += ((objects[hit_id]->material->km.array() * rgb_n.array()).matrix());
    }
    return true;
  }
  return false;
  
}
