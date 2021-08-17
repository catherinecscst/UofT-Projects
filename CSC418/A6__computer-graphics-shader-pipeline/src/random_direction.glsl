// Generate a pseudorandom unit 3D vector
// 
// Inputs:
//   seed  3D seed
// Returns psuedorandom, unit 3D vector drawn from uniform distribution over
// the unit sphere (assuming random2 is uniform over [0,1]²).
//
// expects: random2.glsl, PI.glsl
vec3 random_direction( vec3 seed)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code 
  // return vec3(1,0,0);

  float PI = 3.1415927;
  vec2 result = random2(seed);
  float theta = 2 * PI * result.x; 
  float phi = PI * result.y;

  float x = sin(phi)*cos(theta);
  float y = sin(phi)*sin(theta);
  float z = cos(phi);
 
  return normalize(vec3(x, y, z));

  /////////////////////////////////////////////////////////////////////////////
}
