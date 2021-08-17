#include "write_ppm.h"
#include <fstream>
#include <cassert>
#include <iostream>

bool write_ppm(
  const std::string & filename,
  const std::vector<unsigned char> & data,
  const int width,
  const int height,
  const int num_channels)
{
  ////////////////////////////////////////////////////////////////////////////
  // Replace with your code from computer-graphics-raster-images
  
  assert(
    (num_channels == 3 || num_channels ==1 ) &&
    ".ppm only supports RGB or grayscale images");
  
  // Write an rgb or grayscale image to a .ppm file.

  std::ofstream img;
  img.open(filename, std::ios::binary);
  assert(
    (! img.fail()) &&
    "can not open the file");

  try {
    if (num_channels == 3){
      img << "P6" << std::endl;
    } else {
      img << "P5" << std::endl;
    }
    img << width << " " << height << std::endl << 255 << std::endl;

    for (int i = 0; i < width * height * num_channels; i++){
      img << data[i];
    }
    
    img.close();
    return true;

  } catch (const std::exception & e){
    img.close();
    return false;
  }
  
  return false;
  ////////////////////////////////////////////////////////////////////////////
}
