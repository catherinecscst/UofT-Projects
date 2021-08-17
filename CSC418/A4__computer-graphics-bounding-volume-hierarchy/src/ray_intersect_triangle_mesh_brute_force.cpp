#include "ray_intersect_triangle_mesh_brute_force.h"
#include "ray_intersect_triangle.h"

bool ray_intersect_triangle_mesh_brute_force(
  const Ray & ray,
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & F,
  const double min_t,
  const double max_t,
  double & hit_t,
  int & hit_f)
{
  // Shoot a ray at a triangle mesh with faces and record the closest hit. 
  // Use a brute force loop over all triangles, aim for complexity but focus on correctness. 
  // This will be your reference solution.

  hit_t = std::numeric_limits<double>::infinity();
  hit_f = -1;

  for(int i = 0; i < F.rows(); i++){
    double curr_t;
    if (ray_intersect_triangle(ray, V.row(F(i,0)), V.row(F(i,1)), V.row(F(i,2)), min_t, max_t, curr_t)){
      if (curr_t < hit_t){
        hit_t = curr_t;
        hit_f = i;
      }
    }
  }

  if (hit_f != -1){
    return true;
  }
  return false;

}
