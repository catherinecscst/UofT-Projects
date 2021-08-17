#include "sphere.h"
#include <iostream>
#include <math.h>

void sphere(
  const int num_faces_u,
  const int num_faces_v,
  Eigen::MatrixXd & V,
  Eigen::MatrixXi & F,
  Eigen::MatrixXd & UV,
  Eigen::MatrixXi & UF,
  Eigen::MatrixXd & NV,
  Eigen::MatrixXi & NF)
{
  
  // Construct a quad mesh of a sphere with num_faces_u × num_faces_v faces.

  int all_faces = num_faces_u * num_faces_v;
  int all_vertices = (num_faces_u + 1) * (num_faces_v + 1);
  V.resize(all_vertices, 3);
  F.resize(all_faces, 4);
  UV.resize(all_vertices, 2);
  UF.resize(all_faces, 4);
  NV.resize(all_vertices, 3);
  NF.resize(all_faces, 4);

  int face_count = 0;
  for (int i = 0; i < num_faces_u; i++){
    for (int j = 0; j < num_faces_v; j++){

      int v1 = i * (num_faces_v + 1) + j;
      int v2 = (i + 1) * (num_faces_v + 1) + j;
      int v3 = (i + 1) * (num_faces_v + 1) + j + 1;
      int v4 = i * (num_faces_v + 1) + j + 1;

      F.row(face_count) = Eigen::RowVector4i(v1, v2, v3, v4);
      UF.row(face_count) = Eigen::RowVector4i(v1, v2, v3, v4);
      NF.row(face_count) = Eigen::RowVector4i(v1, v2, v3, v4);
      face_count++;
    }
  }

  int vertex_count = 0;
  for (int i = 0; i < num_faces_u + 1; i++){
    for (int j = 0; j < num_faces_v + 1; j++){

      double theta = static_cast<double>(i) / num_faces_u * M_PI * 2.0;
      double phi = static_cast<double>(j) / num_faces_v * M_PI;
      double x = -sin(phi) * cos(theta);
      double y = -sin(phi) * sin(theta);
      double z = -cos(phi);

      V.row(vertex_count) = Eigen::RowVector3d(x, y, z);
      double uu = static_cast<double>(i) / num_faces_u;
      double vv = static_cast<double>(j) / num_faces_v;
      UV.row(vertex_count) = Eigen::RowVector2d(uu, vv);
      NV.row(vertex_count) = Eigen::RowVector3d(x, y, z);
      vertex_count++;
    }
  }

}
