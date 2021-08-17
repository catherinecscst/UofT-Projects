#include "reflect.h"

void reflect(
  const std::vector<unsigned char> & input,
  const int width,
  const int height,
  const int num_channels,
  std::vector<unsigned char> & reflected)
{
  reflected.resize(width*height*num_channels);
  
  //Horizontally reflect an image (like a mirror)

  for (int i = 0; i < height; i++){
  	int n = 1;
    for (int j = 0; j < width * num_channels; j++){
      if (num_channels == 3) {  // rbg
        if (j % num_channels == 0) {
          reflected[ 3 * i * width + j] = input[ 3 * (i + 1) * width - 3 * n];
          reflected[3 * i * width + j + 1] = input[3 * (i + 1) * width - 3 * n + 1];
          reflected[3 * i * width + j + 2] = input[3 * (i + 1) * width - 3 * n + 2];
          n ++;
        }
      } 
      else if (num_channels == 1) {  // grayscale
        reflected[i * width + j] = input[(i + 1) * width - 3 * n];
        n ++;
      }
    }
  }

}
