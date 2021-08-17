#include "simulate_bayer_mosaic.h"

void simulate_bayer_mosaic(
  const std::vector<unsigned char> & rgb,
  const int & width,
  const int & height,
  std::vector<unsigned char> & bayer)
{
  bayer.resize(width*height);
  
  //Simulate an image acquired from the Bayer mosaic by taking a 3-channel rgb image 
  // and creating a single channel grayscale image composed of interleaved red/green/blue channels. 
  // The output image should be the same size as the input but only one channel.

  for (int i = 0; i < height; i++){
      for (int j = 0; j < width; j++){
      	int n = i * width + j;
        if (i % 2 == 0){ // gb
          if (j % 2 == 0){
            bayer[n] = rgb[n * 3 + 1];
          }
          else{
            bayer[n] = rgb[(n) * 3 + 2];
          }
        }
        else{ // rg
          if (j % 2 == 0){
            bayer[n] = rgb[(n) * 3];
          }
          else{
            bayer[n] = rgb[(n) * 3 + 1];
          }
        }
      }
  }

}
