#include "rgb_to_gray.h"

void rgb_to_gray(
  const std::vector<unsigned char> & rgb,
  const int width,
  const int height,
  std::vector<unsigned char> & gray)
{
  gray.resize(height*width);

  //Convert a 3-channel RGB image to a 1-channel grayscale image.

  for (int i = 0; i < height; i++){
    for (int j = 0; j < width; j++){
      int n = i * width + j;
      gray[n] = (unsigned char)(0.2126 * (double)rgb[3 * n] + 
      	                        0.7152 * (double)rgb[3 * n + 1] + 
      	                        0.0722 * (double)rgb[3 * n + 2]);
    }
  }

}


