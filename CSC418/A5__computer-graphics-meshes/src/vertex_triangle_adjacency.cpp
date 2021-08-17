#include "vertex_triangle_adjacency.h"

void vertex_triangle_adjacency(
  const Eigen::MatrixXi & F,
  const int num_vertices,
  std::vector<std::vector<int> > & VF)
{
  
  // Compute a vertex-triangle adjacency list. For each vertex store a list of all incident faces.

  VF.resize(num_vertices);
  
  for (int i = 0; i < F.rows(); i++){
    for (int j = 0; j < F.cols(); j++){
      VF[F(i, j)].push_back(i);
    }
  }

}

