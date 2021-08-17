// Set the pixel color using Blinn-Phong shading (e.g., with constant blue and
// gray material color) with a bumpy texture.
// 
// Uniforms:
uniform mat4 view;
uniform mat4 proj;
uniform float animation_seconds;
uniform bool is_moon;
// Inputs:
//                     linearly interpolated from tessellation evaluation shader
//                     output
in vec3 sphere_fs_in;
in vec3 normal_fs_in;
in vec4 pos_fs_in; 
in vec4 view_pos_fs_in; 
// Outputs:
//               rgb color of this pixel
out vec3 color;
// expects: model, blinn_phong, bump_height, bump_position,
// improved_perlin_noise, tangent
void main()
{
  /////////////////////////////////////////////////////////////////////////////
  // Replace with your code 
  // color = vec3(1,1,1);

  float PI = 3.1415927;
  float theta = PI / 4.0 * animation_seconds;

  vec4 point_light = view * vec4(6 * cos(theta), 2, 6 * sin(theta), 1);
  vec3 point_light_3d = point_light.xyz / point_light.w;
  
  vec3 vp = view_pos_fs_in.xyz / view_pos_fs_in.w;
  vec3 T, B;
  tangent(normalize(sphere_fs_in), T, B);
  mat4 m = model(is_moon, animation_seconds);
  vec3 b_sphere_fs_in = bump_position(is_moon, sphere_fs_in);
  vec3 n = normalize(cross(
             (bump_position(is_moon, sphere_fs_in + T * 0.0001) - b_sphere_fs_in) / 0.0001, 
             (bump_position(is_moon, sphere_fs_in + B * 0.0001) - b_sphere_fs_in) / 0.0001));
  if (dot(sphere_fs_in, n) < 0){
    n = -n;
  }
  vec3 normal = (transpose(inverse(view)) * transpose(inverse(m)) * vec4(n, 1)).xyz;
  if (is_moon){
    color = blinn_phong(vec3(0.05, 0.05, 0.05),vec3(0.5, 0.5, 0.5),vec3(1, 1, 1),1000,normalize(normal),normalize(-vp),normalize(point_light_3d-vp));
  }
  else{
    color = blinn_phong(vec3(0.05, 0.05, 0.05),vec3(0.2, 0.2, 0.8),vec3(1, 1, 1),1000,normalize(normal),normalize(-vp),normalize(point_light_3d-vp));
  }

  /////////////////////////////////////////////////////////////////////////////
}
