#include "Triangle.h"
#include "Ray.h"

bool Triangle::intersect(
  const Ray & ray, const double min_t, double & t, Eigen::Vector3d & n) const
{
  
  // Intersect a triangle with a ray.
  
  Eigen::Vector3d pA = std::get<0>(corners);
  Eigen::Vector3d pB = std::get<1>(corners);
  Eigen::Vector3d pC = std::get<2>(corners);
  Eigen::Vector3d b_a = pB-pA;
  Eigen::Vector3d c_a = pC-pA;

  double a = pA[0] - pB[0];
  double b = pA[1] - pB[1];
  double c = pA[2] - pB[2];
  double d = pA[0] - pC[0];
  double e = pA[1] - pC[1];
  double f = pA[2] - pC[2];
  double g = ray.direction[0];
  double h = ray.direction[1];
  double i = ray.direction[2];
  double j = pA[0] - ray.origin[0];
  double k = pA[1] - ray.origin[1];
  double l = pA[2] - ray.origin[2];

  double ei_hf = (e * i - h * f);
  double gf_di = (g * f - d * i);
  double dh_eg = (d * h - e * g);
  double ak_jb = (a * k - j * b);
  double jc_al = (j * c - a * l);
  double bl_kc = (b * l - k * c);

  double m = a* ei_hf +b* gf_di +c* dh_eg;
  double t_out = - (f * ak_jb + e * jc_al + d * bl_kc) / m;

  if (t_out < min_t){
    return false;
  }

  double gamma = (i * ak_jb + h * jc_al +g * bl_kc) / m;
  double beta = (j * ei_hf + k * gf_di + l * dh_eg)/m;

  if (gamma >= 0 && beta >= 0 && beta + gamma <= 1) {
  	t = t_out;
	n = b_a.cross(c_a).normalized();
    return true;
  }

  return false;
}


