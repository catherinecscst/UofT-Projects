#include "desaturate.h"
#include "hsv_to_rgb.h"
#include "rgb_to_hsv.h"

void desaturate(
  const std::vector<unsigned char> & rgb,
  const int width,
  const int height,
  const double factor,
  std::vector<unsigned char> & desaturated)
{
  desaturated.resize(rgb.size());
  
  // Desaturate a given rgb color image by a given factor.

  int n = 0, m = 0;
  for (int i = 0; i < height; i++){
    for (int j = 0; j < width; j++){
      double r, g, b;
      r = (double)(rgb[n]) / 255.0, g = (double)(rgb[n + 1]) / 255.0, b = (double)(rgb[n + 2]) / 255.0;
      double h, s, v;
      rgb_to_hsv(r, g, b, h, s, v);
      s *= (1.0 - factor);
      hsv_to_rgb(h, s, v, r, g, b);
      desaturated[m] = r * 255.0, desaturated[m + 1] = g * 255.0, desaturated[m + 2] = b * 255.0;
      n += 3;
      m += 3;
    }
  }

}
