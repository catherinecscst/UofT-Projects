#include "catmull_clark.h"
#include <unordered_map>
#include <utility>
#include <functional>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>

void catmull_clark(
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & F,
  const int num_iters,
  Eigen::MatrixXd & SV,
  Eigen::MatrixXi & SF)
{

  // SV = V;
  // SF = F;

  // Replace with your code here:
  if (num_iters == 0){
    return;
  }

  std::unordered_map<int, Eigen::RowVector3d> face_point;
  std::unordered_map<int, std::vector<int>> point_adjfaces;
  std::unordered_map<int, std::vector<int>> point_neighbour;
  std::unordered_map<std::string, std::vector<int>> edge_adjfaces;

  for (int i = 0; i < F.rows(); i++){

    Eigen::RowVector3d accumulator(0, 0, 0);

    for (int j = 0; j < F.cols(); j++){

      int pt = F(i, j);

      accumulator += V.row(pt);
      point_adjfaces[pt].emplace_back(i);

      //edge to faces
      std::string key1, key2;
      key1 = std::to_string(pt) + "-" + std::to_string(F(i, (j + 1) % F.cols()));
      key2 = std::to_string(F(i, (j + 1) % F.cols())) + "-" + std::to_string(pt);

      if (std::find(edge_adjfaces[key1].begin(), edge_adjfaces[key1].end(), i) == edge_adjfaces[key1].end()){
        edge_adjfaces[key1].push_back(i);
      }
      if (std::find(edge_adjfaces[key2].begin(), edge_adjfaces[key2].end(), i) == edge_adjfaces[key2].end()){
        edge_adjfaces[key2].push_back(i);
      }

      //point to neighbour
      int neighbor1, neighbor2;
      neighbor1 = F(i, (j + 1) % F.cols());
      neighbor2 = F(i, (j - 1 + F.cols()) % F.cols());

      if (std::find(point_neighbour[pt].begin(), point_neighbour[pt].end(), neighbor1) == point_neighbour[pt].end()){
        point_neighbour[pt].push_back(neighbor1);
      }
      if (std::find(point_neighbour[pt].begin(), point_neighbour[pt].end(), neighbor2) == point_neighbour[pt].end()){
        point_neighbour[pt].push_back(neighbor2);
      }
    }

    //face_point
    face_point[i] = accumulator / 4.0;
  }

  
  SV.resize(0, 3);
  SF.resize(0, 4);
  for (int i = 0; i < F.rows(); i++){
    for (int j = 0; j < F.cols(); j++){

      int pt = F(i, j);

      Eigen::RowVector3d fp = face_point[i];
      
      // edge point
      int pt_1 = F(i, (j + 1) % F.cols());
      int pt_2 = F(i, ((j - 1) + F.cols()) % F.cols());
      std::string pt_1_key = std::to_string(pt) + "-" + std::to_string(pt_1);
      std::string pt_2_key = std::to_string(pt) + "-" + std::to_string(pt_2);
      Eigen::RowVector3d edgepoint1(0, 0, 0), edgepoint2(0, 0, 0);
      for (int k: edge_adjfaces[pt_1_key]){
         edgepoint1 += face_point[k];
      }
      for (int k: edge_adjfaces[pt_2_key]){
         edgepoint2 += face_point[k];
      }
      edgepoint1 += V.row(pt) + V.row(pt_1);
      edgepoint1 /= 4.0;

      edgepoint2 += V.row(pt) + V.row(pt_2);
      edgepoint2 /= 4.0;

      Eigen::RowVector3d edge_point_1 = edgepoint1;
      Eigen::RowVector3d edge_point_2 = edgepoint2;

      // update original vertex point
      Eigen::RowVector3d org = V.row(pt);
      Eigen::RowVector3d avg_face(0, 0, 0);
      double nf = point_adjfaces[pt].size();
      double nn = point_neighbour[pt].size();

      for (int k: point_adjfaces[pt]){
        avg_face += face_point[k];
      }
      avg_face /= nf;

      Eigen::RowVector3d avg_edge(0, 0, 0);
      for (int neighbor_idx: point_neighbour[pt]){
        avg_edge += (V.row(pt) + V.row(neighbor_idx))/2.0;
      }
      avg_edge /= nn;

      Eigen::RowVector3d new_vpoint = (avg_face + 2.0 * avg_edge + (nf - 3) * org) / nf;

      //construct new sv and sf
      Eigen::RowVector4i newfaces(-1, -1, -1, -1);
      int count = 0;
      for (auto vertex:{fp, edge_point_1, edge_point_2, new_vpoint}){
        for (int k = 0; k < SV.rows(); k++){
          if (vertex.isApprox(SV.row(k))){
            newfaces(count) = k;
          }
        }
        if (newfaces(count) == -1){
            SV.conservativeResize(SV.rows() + 1, Eigen::NoChange);
            SV.row(SV.rows() - 1) = vertex;
            newfaces(count) = SV.rows() - 1;
          }
          count++;
        }
        SF.conservativeResize(SF.rows() + 1, Eigen::NoChange);
        SF.row(SF.rows() - 1) = newfaces;
    }
  }

  //recursive call
  catmull_clark(Eigen::MatrixXd(SV), Eigen::MatrixXi(SF), num_iters - 1, SV, SF);
  ////////////////////////////////////////////////////////////////////////////
}
