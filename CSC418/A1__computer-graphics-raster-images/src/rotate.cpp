#include "rotate.h"

void rotate(
  const std::vector<unsigned char> & input,
  const int width,
  const int height,
  const int num_channels,
  std::vector<unsigned char> & rotated)
{
  rotated.resize(height*width*num_channels);
  
  //Rotate an image 90^\circ counter-clockwise

  int n = 0;
  for (int i = width - 1; i >= 0; i--) {
    for (int j = 0; j < height * num_channels; j++) {
      	if (num_channels == 3) {  // rbg
	        if (j % num_channels == 0) {
	        	rotated[n] = input[3 * (width * (j / 3) + i)];
	          	rotated[n + 1] = input[3 * (width * (j / 3) + i) + 1];
	          	rotated[n + 2] = input[3 * (width * (j / 3) + i) + 2];
	          	n +=3;
	        }
      	}
      	else if (num_channels == 1) { // grayscale
      		rotated[n] = input[width*j+i];
      		n += 1;
      	}
    }
  }
  
}
