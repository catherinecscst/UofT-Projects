#include "per_corner_normals.h"
#include "triangle_area_normal.h"
// Hint:
#include "vertex_triangle_adjacency.h"
#include <iostream>
#include <math.h>

void per_corner_normals(
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & F,
  const double corner_threshold,
  Eigen::MatrixXd & N)
{
  
  // Compute per corner normals for a triangle mesh 
  // by computing the area-weighted average of normals at incident faces 
  // whose normals deviate less than the provided threshold.

  N = Eigen::MatrixXd::Zero(F.rows()*3,3);
  
  std::vector<std::vector<int>> VF;
  vertex_triangle_adjacency(F, V.rows(), VF);

  for (int i = 0; i < F.rows(); i++){
    for (int j = 0; j < F.cols(); j++){

      double areas = 0;
      Eigen::RowVector3d vn(0, 0, 0);
      Eigen::RowVector3d curr_fn = triangle_area_normal(V.row(F(i, 0)), V.row(F(i, 1)), V.row(F(i, 2)));
      
      for (int k : VF[F(i, j)]){

        Eigen::RowVector3d curr_adjn = triangle_area_normal(V.row(F(k, 0)), V.row(F(k, 1)), V.row(F(k, 2)));
        
        double fn = (curr_fn.normalized()).dot(curr_adjn.normalized());
        if (fn > cos(corner_threshold * M_PI / 180.0)){
          areas += curr_adjn.norm();
          vn += curr_adjn;
        }
      }

      N.row(i * 3 + j) = (vn / areas).normalized();
    }
  }

}
