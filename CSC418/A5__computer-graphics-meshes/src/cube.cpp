#include "cube.h"

void cube(
  Eigen::MatrixXd & V,
  Eigen::MatrixXi & F,
  Eigen::MatrixXd & UV,
  Eigen::MatrixXi & UF,
  Eigen::MatrixXd & NV,
  Eigen::MatrixXi & NF)
{

  // Construct the quad mesh of a cube including parameterization and per-face normals.

  ////Hint:
  V.resize(8,3);
  F.resize(6,4);
  UV.resize(14,2);
  UF.resize(6,4);
  NV.resize(6,3);
  NF.resize(6,4);

  V << 0,0,0,
       0,1,0,
       1,1,0,
       1,0,0,
       0,0,1,
       0,1,1,
       1,1,1,
       1,0,1;

  F << 0,1,2,3,
       0,4,5,1,
       1,5,6,2,
       2,6,7,3,
       0,3,7,4,
       4,7,6,5;

  UV << 0,0.25,
        0.25,0.25,
        0.25,0.5,
        0,0.5,
        0.5,0.25,
        0.5,0.5,
        0.5,0.75,
        0.25,0.75,
        0.25,0,
        0.5,0,
        0.75,0.5,
        0.75,0.25,
        1,0.25,
        1,0.5;

  UF << 1,8,9,4,
        1,2,3,0,
        12,13,10,11,
        11,10,5,4,
        1,4,5,2,
        2,5,6,7;

  NV << 0,0,-1,
        -1,0,0,
        0,1,0,
        1,0,0,
        0,-1,0,
        0,0,1;

  NF << 0,0,0,0,
        1,1,1,1,
        2,2,2,2,
        3,3,3,3,
        4,4,4,4,
        5,5,5,5;
}
