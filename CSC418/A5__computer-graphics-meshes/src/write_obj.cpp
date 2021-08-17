#include "write_obj.h"
#include <fstream>
#include <cassert>
#include <iostream>

bool write_obj(
  const std::string & filename,
  const Eigen::MatrixXd & V,
  const Eigen::MatrixXi & F,
  const Eigen::MatrixXd & UV,
  const Eigen::MatrixXi & UF,
  const Eigen::MatrixXd & NV,
  const Eigen::MatrixXi & NF)
{

  // Write a pure-triangle or pure-quad mesh with 3D vertex positions V and faces F, 
  // 2D parametrization positions UV and faces UF, 3D normal vectors NV and faces NF to a .obj file.
  assert((F.size() == 0 || F.cols() == 3 || F.cols() == 4) && "F must have 3 or 4 columns");

  // open file, failure check
  std::ofstream file;
  file.open(filename, std::ios::binary);
  if (file.fail()){
    std::cout << "Cannot open the file: " << filename << std::endl;
    return false;
  }

  try{

    for (int i = 0; i < V.rows(); i++){
      file << "v " << V(i, 0) << " " << V(i, 1) << " " << V(i, 2) << "\n";
    }
    for (int i = 0; i < UV.rows(); i++){
      file << "vt " << UV(i, 0) << " " << UV(i, 1) << "\n";
    }
    for (int i = 0; i < NV.rows(); i++){
      file << "vn " << NV(i, 0) << " " << NV(i, 1) << " " << NV(i, 2) << "\n";
    }

    for (int i = 0; i < F.rows(); i++){
      file << "f ";
      for (int j = 0; j < F.cols(); j++){
        file << F(i, j) + 1 << "/" << UF(i, j) + 1 << "/" << NF(i, j) + 1 << " ";
      }
      file << "\n";
    }

    return true;

  } catch (const char *e) {
    //fprintf(stderr, "%s\n", e);
    file.close();
  }

  return false;

}
