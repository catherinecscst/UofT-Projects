// Input:
//   N  3D unit normal vector
// Outputs:
//   T  3D unit tangent vector
//   B  3D unit bitangent vector
void tangent(in vec3 N, out vec3 T, out vec3 B)
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code 
  T = vec3(1,0,0);
  B = vec3(0,1,0);

  vec3 c1 = cross(N, vec3(0, 0, 1));
  vec3 c2 = cross(N, vec3(0, 1, 0));

  if (length(c2) > length(c1)){
    T = normalize(c1);
    B = normalize(cross(N, c1));
  }
  else{
    T = normalize(c2);
    B = normalize(cross(N, c2));
  }

  /////////////////////////////////////////////////////////////////////////////
}
