#include "hue_shift.h"
#include "hsv_to_rgb.h"
#include "rgb_to_hsv.h"
#include <cmath>

void hue_shift(
  const std::vector<unsigned char> & rgb,
  const int width,
  const int height,
  const double shift,
  std::vector<unsigned char> & shifted)
{
  shifted.resize(rgb.size());

  // Shift the hue of a color rgb image.

  int n = 0, m = 0;
  for (int i = 0; i < height; i++){
    for (int j = 0; j < width; j++){
      double r, g, b;
      r = (double)(rgb[n]) / 255.0, g = (double)(rgb[n + 1]) / 255.0, b = (double)(rgb[n + 2]) / 255.0;
      double h, s, v = 0;
      rgb_to_hsv(r, g, b, h, s, v);
      h += shift;
      while (h < 0){
        h += 360.0;
      }
      h = std::fmod(h, 360.0);
      hsv_to_rgb(h, s, v, r, g, b);
      shifted[m] = r * 255.0, shifted[m + 1] = g * 255.0, shifted[m + 2] = b * 255.0;
      n += 3, m += 3;
    }
  }
}
