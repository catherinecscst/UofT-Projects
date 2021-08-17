#include "catmull_rom_interpolation.h"
#include <Eigen/Dense>

Eigen::Vector3d catmull_rom_interpolation(
  const std::vector<std::pair<double, Eigen::Vector3d> > & keyframes,
  double t)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code
  // return Eigen::Vector3d(0,0,0);
  //////////////////////////////

  if (keyframes.size() == 0) {
  	return Eigen::Vector3d(0, 0, 0);
  }
  
  // circular t
  t = fmod(t, keyframes.back().first);

  int findidx;
  for (findidx = 0; findidx < keyframes.size(); findidx++){
    if (keyframes[findidx].first > t){
      // found index
      break;
    }
  }

  // index at 0, 1 and -1
  if (findidx < 2 || findidx == keyframes.size() - 1){
    double t0, t1;
    Eigen::Vector3d P0, P1;

    t0 = keyframes[findidx - 1].first;
    P0 = keyframes[findidx - 1].second;

    t1 = keyframes[findidx].first;
    P1 = keyframes[findidx].second;

    double mu = (1 - cos(((t - t0)/(t1 - t0)) * M_PI)) / 2;
    return (P0 * (1 - mu) + P1 * mu);
  }

  double t0, t1, t2, t3;
  Eigen::Vector3d P0, P1, P2, P3;

  t0 = keyframes[findidx - 2].first;
  P0 = keyframes[findidx - 2].second;

  t1 = keyframes[findidx - 1].first;
  P1 = keyframes[findidx - 1].second;

  t2 = keyframes[findidx].first;
  P2 = keyframes[findidx].second;

  t3 = keyframes[findidx + 1].first;
  P3 = keyframes[findidx + 1].second;

  Eigen::Vector3d t_01 = (t1 - t)/(t1 - t0) * P0 + (t - t0)/(t1 - t0) * P1;
  Eigen::Vector3d t_12 = (t2 - t)/(t2 - t1) * P1 + (t - t1)/(t2 - t1) * P2;
  Eigen::Vector3d t_23 = (t3 - t)/(t3 - t2) * P2 + (t - t2)/(t3 - t2) * P3;

  Eigen::Vector3d c = (t2 - t)/(t2 - t1) * ((t2 - t)/(t2 - t0) * t_01 + (t - t0)/(t2 - t0) * t_12) 
                    + (t - t1)/(t2 - t1) * ((t3 - t)/(t3 - t1) * t_12 + (t - t1)/(t3 - t1) * t_23);

  return c;

  /////////////////////////////////////////////////////////////////////////////
}
