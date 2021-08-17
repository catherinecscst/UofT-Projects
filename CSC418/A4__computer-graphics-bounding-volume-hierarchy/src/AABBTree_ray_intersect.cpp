#include "AABBTree.h"

// See AABBTree.h for API
bool AABBTree::ray_intersect(
  const Ray& ray,
  const double min_t,
  const double max_t,
  double & t,
  std::shared_ptr<Object> & descendant) const 
{
  
  // Determine whether and how a ray intersects the contents of an AABB tree. 
  // The method should perform in  time for a tree containing  (reasonably distributed) objects.

  if (ray_intersect_box(ray, this->box, min_t, max_t)){

    double left_t, right_t;
    std::shared_ptr<Object> left_nxt, right_nxt;

    bool left_hit = (this->left != NULL) && (this->left->ray_intersect(ray, min_t, max_t, left_t, left_nxt));
    bool right_hit = (this->right != NULL) && (this->right->ray_intersect(ray, min_t, max_t, right_t, right_nxt));

    if (left_hit && !left_nxt){
      left_nxt = this->left;
    }
    if (right_hit && !right_nxt){
      right_nxt = this->right;
    }

    if (left_hit && right_hit){

      if (left_t < right_t){
        t = left_t;
        descendant = left_nxt;
      }
      else{
        t = right_t;
        descendant = right_nxt;
      }
      return true;
    }
    else if (left_hit){

      t = left_t;
      descendant = left_nxt;
      return true;
    }
    else if (right_hit){

      t = right_t;
      descendant = right_nxt;
      return true;
    }   
  }
  
  return false;

}

