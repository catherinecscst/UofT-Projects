#include "over.h"

void over(
  const std::vector<unsigned char> & A,
  const std::vector<unsigned char> & B,
  const int & width,
  const int & height,
  std::vector<unsigned char> & C)
{
  C.resize(A.size());
  
  // Compute C = A Over B, where A and B are semi-transparent rgba images and "Over" is the Porter-Duff Over operator.

  int a = 0, b = 0, c = 0;
  for (int x = 0; x < height; x++){
    for (int y = 0; y < width; y++){
      double A_r, A_g, A_b, A_a;
      double B_r, B_g, B_b, B_a;

      A_r = (double)A[a];
      A_g = (double)A[a + 1];
      A_b = (double)A[a + 2];
      A_a = (double)A[a + 3] / 255.0;
      a += 4;
      
      B_r = (double)B[b];
      B_g = (double)B[b + 1];
      B_b = (double)B[b + 2];
      B_a = (double)B[b + 3] / 255.0;
      b += 4;

      double r = ((A_a * A_r) + (1.0 - A_a) * B_a * B_r) / (A_a + B_a * (1.0 - A_a));
      double g = ((A_a * A_g) + (1.0 - A_a) * B_a * B_g) / (A_a + B_a * (1.0 - A_a));
      double b = ((A_a * A_b) + (1.0 - A_a) * B_a * B_b) / (A_a + B_a * (1.0 - A_a));

      C[c] = r, C[c + 1] = g, C[c + 2] = b, C[c + 3] = (A_a + B_a * (1.0 - A_a)) * 255.0;
      c += 4;
    }
  }
}
