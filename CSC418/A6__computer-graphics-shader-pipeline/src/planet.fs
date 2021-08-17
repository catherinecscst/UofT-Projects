// Generate a procedural planet and orbiting moon. Use layers of (improved)
// Perlin noise to generate planetary features such as vegetation, gaseous
// clouds, mountains, valleys, ice caps, rivers, oceans. Don't forget about the
// moon. Use `animation_seconds` in your noise input to create (periodic)
// temporal effects.
//
// Uniforms:
uniform mat4 view;
uniform mat4 proj;
uniform float animation_seconds;
uniform bool is_moon;
// Inputs:
in vec3 sphere_fs_in;
in vec3 normal_fs_in;
in vec4 pos_fs_in; 
in vec4 view_pos_fs_in; 
// Outputs:
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

  vec3 sphere_fs_in_b = bump_position(is_moon, sphere_fs_in);
  vec3 T_b = (bump_position(is_moon, sphere_fs_in + T * 0.0001) - sphere_fs_in_b) / 0.0001;
  vec3 B_b = (bump_position(is_moon, sphere_fs_in + B * 0.0001) - sphere_fs_in_b) / 0.0001;
  vec3 n = normalize(cross(T_b, B_b));
  
  if (dot(sphere_fs_in, n) < 0){
    n = -n;
  }
  mat4 m = model(is_moon, animation_seconds);
  vec3 normal = (transpose(inverse(view * m)) * vec4(n, 1)).xyz;

  float e = PI / 2;
  float clouds = abs(improved_perlin_noise(vec3(
                      sphere_fs_in.x + sin(animation_seconds * PI / 12),
                      sphere_fs_in.y, 
                      0) * e));

  if (is_moon){
    color = blinn_phong(vec3(0.05, 0.05, 0.05),vec3(0.5, 0.5, 0.5), vec3(1, 1, 1), 1000, normalize(normal), normalize(-vp), normalize(point_light_3d-vp));
  }
  else{
    if (bump_height(is_moon, sphere_fs_in) < 0.03){ //ocean
      vec3 ka = vec3(0.05, 0.05, 0.05);
      vec3 kd = vec3(0.2, 0.2, 0.8) * (1 - clouds) + clouds * vec3(1 , 1, 1);
      vec3 ks = vec3(1, 1, 1);
      color = blinn_phong(ka, kd, ks, 1000, normalize(normal), normalize(-vp), normalize(point_light_3d - vp));
    }
    else if (bump_height(is_moon, sphere_fs_in) > 0.18){ // higher lands
      vec3 ka = vec3(0.05, 0.05, 0.05);
      vec3 kd = vec3(0.8, 0.7, 0.1) * (1 - clouds) + clouds * vec3(1 , 1, 1);
      vec3 ks = vec3(1, 1, 1);
      color = blinn_phong(ka, kd, ks, 1000, normalize(normal), normalize(-vp), normalize(point_light_3d - vp));
    }
    else{ //greens
      vec3 ka = vec3(0.05, 0.05, 0.05);
      vec3 kd = vec3(0.2, 0.7, 0.1) * (1 - clouds) + clouds * vec3(1, 1, 1);
      vec3 ks = vec3(1, 1, 1);
      color = blinn_phong(ka, kd, ks, 1000, normalize(normal), normalize(-vp), normalize(point_light_3d - vp));
    }
  }

  /////////////////////////////////////////////////////////////////////////////
}
