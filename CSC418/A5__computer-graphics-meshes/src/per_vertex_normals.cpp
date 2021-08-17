#include "per_vertex_normals.h"
#include "triangle_area_normal.h"
#include <unordered_map>
#include <list>

void per_vertex_normals(
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & F,
  Eigen::MatrixXd & N)
{
  
  // Compute per-vertex normals for a triangle mesh.
  
  std::unordered_map<int, std::list<int>> adj_faces;
  for (int i = 0; i < F.rows(); i++) {
    for (int j = 0; j < F.cols(); j++) {
      adj_faces[F(i, j)].emplace_back(i);
    }
  }

  N = Eigen::MatrixXd::Zero(V.rows(),3);

  for (int i = 0; i < V.rows(); i++){
    double areas = 0;
    Eigen::RowVector3d normals(0, 0, 0);
    for (int k : adj_faces[i]){

      Eigen::RowVector3d tri_area_n = triangle_area_normal(V.row(F(k, 0)), V.row(F(k, 1)), V.row(F(k, 2)));
      normals += tri_area_n;
      areas += tri_area_n.norm();
    }
    N.row(i) = (normals / areas).normalized();
  }
  
}
