#include "ray_intersect_triangle.h"

bool ray_intersect_triangle(
  const Ray & ray,
  const Eigen::RowVector3d & A,
  const Eigen::RowVector3d & B,
  const Eigen::RowVector3d & C,
  const double min_t,
  const double max_t,
  double & t)
{

  // Intersect a ray with a triangle.

  double a = A[0] - B[0];
  double b = A[1] - B[1];
  double c = A[2] - B[2];
  double d = A[0] - C[0];
  double e = A[1] - C[1];
  double f = A[2] - C[2];
  double g = ray.direction[0];
  double h = ray.direction[1];
  double i = ray.direction[2];
  double j = A[0] - ray.origin[0];
  double k = A[1] - ray.origin[1];
  double l = A[2] - ray.origin[2];

  double ei_hf = (e * i - h * f);
  double gf_di = (g * f - d * i);
  double dh_eg = (d * h - e * g);
  double ak_jb = (a * k - j * b);
  double jc_al = (j * c - a * l);
  double bl_kc = (b * l - k * c);

  double m = a * ei_hf + b * gf_di + c * dh_eg;
  t = - (f * ak_jb + e * jc_al + d * bl_kc) / m;

  if (t < min_t || t >= max_t){
    return false;
  }

  double gamma = (i * ak_jb + h * jc_al +g * bl_kc) / m;
  double beta = (j * ei_hf + k * gf_di + l * dh_eg)/m;

  if (gamma < 0 || gamma > 1){
    return false;
  }
  if (beta < 0 || beta + gamma > 1){
    return false;
  }

  return true;

}

