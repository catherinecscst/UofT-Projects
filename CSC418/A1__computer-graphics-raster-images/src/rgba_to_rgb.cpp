#include "rgba_to_rgb.h"

void rgba_to_rgb(
  const std::vector<unsigned char> & rgba,
  const int & width,
  const int & height,
  std::vector<unsigned char> & rgb)
{
  rgb.resize(height*width*3);

  // Extract the 3-channel rgb data from a 4-channel rgba image.
  
  for (int i=0; i<height*width; i++) {
  	rgb[3*i] = rgba[4*i];
  	rgb[3*i+1] = rgba[4*i+1];
  	rgb[3*i+2] = rgba[4*i+2];
  }
}
