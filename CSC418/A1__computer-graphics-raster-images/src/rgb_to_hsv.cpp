#include "rgb_to_hsv.h"
#include <cmath>

void rgb_to_hsv(
  const double r,
  const double g,
  const double b,
  double & h,
  double & s,
  double & v)
{
  
  // Convert a color represented by red, green and blue intensities to its representation using hue, saturation and value.

  h = 0;
  s = 0;
  v = 0;

  double max = std::fmax(std::fmax(r, g), b);
  double min = std::fmin(std::fmin(r, g), b);

  if (max == r){
    h += ((g - b) / (max - min)) * 60.0;
  }
  else if (max == g){
    h += ((b - r) / (max - min) + 2.0) * 60.0;
  }
  else if (max == b){
    h += ((r - g) / (max - min) + 4.0) * 60.0;
  }
  
  if (max != 0.0){
    s += (max - min) / max;
  }

  if (h < 0.0){
    h += 360.0;
  }
  v = max;

}
