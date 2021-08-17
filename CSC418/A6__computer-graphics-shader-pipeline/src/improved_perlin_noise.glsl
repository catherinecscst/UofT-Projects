// Given a 3d position as a seed, compute an even smoother procedural noise
// value. "Improving Noise" [Perlin 2002].
//
// Inputs:
//   st  3D seed
// Values between  -½ and ½ ?
//
// expects: random_direction, improved_smooth_step
float improved_perlin_noise( vec3 st) 
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code 
  // return 0;


  vec3 stl = floor(st);
  vec3 sth = ceil(st);

  // 8 corners
  vec3 c1 = vec3(stl.x, stl.y, stl.z);
  vec3 c2 = vec3(sth.x, stl.y, stl.z);
  vec3 c3 = vec3(stl.x, sth.y, stl.z);
  vec3 c4 = vec3(sth.x, sth.y, stl.z);
  vec3 c5 = vec3(stl.x, stl.y, sth.z);
  vec3 c6 = vec3(sth.x, stl.y, sth.z);
  vec3 c7 = vec3(stl.x, sth.y, sth.z);
  vec3 c8 = vec3(sth.x, sth.y, sth.z);

 // random direction of 8 corners
  vec3 rd1 = random_direction(c1);
  vec3 rd2 = random_direction(c2);
  vec3 rd3 = random_direction(c3);
  vec3 rd4 = random_direction(c4);
  vec3 rd5 = random_direction(c5);
  vec3 rd6 = random_direction(c6);
  vec3 rd7 = random_direction(c7);
  vec3 rd8 = random_direction(c8);

  // projections
  float proj1 = dot(st - c1, rd1);
  float proj2 = dot(st - c2, rd2);
  float proj3 = dot(st - c3, rd3);
  float proj4 = dot(st - c4, rd4);
  float proj5 = dot(st - c5, rd5);
  float proj6 = dot(st - c6, rd6);
  float proj7 = dot(st - c7, rd7);
  float proj8 = dot(st - c8, rd8);


  vec3 smooth_f = improved_smooth_step(st - vec3(stl.x, stl.y, stl.z));

  float p1 = smooth_f.z * (proj5 - proj1) + proj1;
  float p2 = smooth_f.z * (proj6 - proj2) + proj2;
  float p3 = smooth_f.z * (proj7 - proj3) + proj3;
  float p4 = smooth_f.z * (proj8 - proj4) + proj4;

  float t5 = smooth_f.y * (p3 - p1) + p1;
  float t6 = smooth_f.y * (p4 - p2) + p2;

  return 2 * (smooth_f.x * (t6 - t5) + t5) / sqrt(3);

  /////////////////////////////////////////////////////////////////////////////
}

