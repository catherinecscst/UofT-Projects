#include "demosaic.h"

void demosaic(
  const std::vector<unsigned char> & bayer,
  const int & width,
  const int & height,
  std::vector<unsigned char> & rgb)
{
  rgb.resize(width*height*3);
  
  // Given a mosaiced image (interleaved GBRG colors in a single channel), created a 3-channel rgb image.

  int n = 0;
  for (int i = 0; i < height; i++){
    for (int j = 0; j < width; j++){
      int m = i * width + j;
      int r = 0, g = 0, b = 0;
      double rr = 0, gg = 0, bb = 0;

      for (int x = -1; x < 2; x++){
        for (int y = -1; y < 2; y++){
          int ix = i + x, jy = j + y;

          if ((ix >= 0 && jy >= 0) && 
          	 (ix < height && jy < width)){
          	int mm = ix * width + jy;

            if(ix % 2 == 0){ // gb
              if(jy % 2 == 0){
                gg += bayer[mm];
                g++;
              }
              else{
                bb += bayer[mm];
                b++;
              }
            }
            else{ // rg
              if(jy % 2 == 0){
                rr += bayer[mm];
                r++;
              }
              else{
                gg += bayer[mm];
                g++;
              }
            }
          }
        }
      }

      if (i % 2 == 0){ // gb
        if (j % 2 == 0){
          rgb[n] = rr/r, rgb[n+1] = bayer[m], rgb[n+2] = bb/b;
          n += 3;
        }
        else{
          rgb[n] = rr/r, rgb[n+1] = gg/g, rgb[n+2] = bayer[m];
          n += 3;
        }
      }
      else{ // rg
        if (j % 2 == 0){
          rgb[n] = bayer[m], rgb[n+1] = gg/g, rgb[n+2] = bb/b;
          n += 3;
        }
        else{
          rgb[n] = rr/r, rgb[n+1] = bayer[m], rgb[n+2] = bb/b;
          n += 3;
        }
      }
    }
  }
  ////////////////////////////////////////////////////////////////////////////
}
