#include "hsv_to_rgb.h"
#include <cmath>

void hsv_to_rgb(
  const double h,
  const double s,
  const double v,
  double & r,
  double & g,
  double & b)
{
  
  // Convert a color represented by hue, saturation and value to its representation using red, green and blue intensities.

  r = 0;
  g = 0;
  b = 0;

  double vs = v * s;
  double hp = h / 60.0;
  double x = vs * (1.0 - std::fabs(std::fmod(hp, 2.0) - 1.0));

  double rp, gp, bp;
  if (0.0 <= hp && hp < 1.0) {
      r += vs;
      g += x;
      b += 0.0;
  } else if (1.0 <= hp && hp < 2.0) {
      r += x;
      g += vs;
      b += 0.0;
  } else if (2.0 <= hp && hp < 3.0) {
      r += 0.0;
      g += vs;
      b += x;
  } else if (3.0 <= hp && hp < 4.0) {
      r += 0.0;
      g += x;
      b += vs;
  } else if (4.0 <= hp && hp < 5.0) {
      r += x;
      g += 0.0;
      b += vs;
  } else if (5.0 <= hp && hp < 6.0) {
      r += vs;
      g += 0.0;
      b += x;
  } else {
      r += 0.0;
      g += 0.0;
      b += 0.0;
  }

  r += (v - vs);
  g += (v - vs);
  b += (v - vs);

}
