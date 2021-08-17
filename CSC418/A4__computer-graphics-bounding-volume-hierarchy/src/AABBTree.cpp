#include "AABBTree.h"
#include "insert_box_into_box.h"

AABBTree::AABBTree(
  const std::vector<std::shared_ptr<Object> > & objects,
  int a_depth): 
  depth(std::move(a_depth)), 
  num_leaves(objects.size())
{
  
  // Construct an axis-aligned bounding box tree given a list of objects. 
  // Use the midpoint along the longest axis of the box containing the given objects to determine the left-right split.
  
  if (objects.empty()){
    this->left = NULL;
    this->right = NULL;
  }
  else if (objects.size() == 1){
    this->left = objects[0];
    this->right = NULL;
    insert_box_into_box(this->left->box, this->box);
  }
  else if (objects.size() == 2){
    this->left = objects[0];
    this->right = objects[1];
    insert_box_into_box(this->left->box, this->box);
    insert_box_into_box(this->right->box, this->box);
  }
  else{

    for (int i = 0; i < objects.size(); i++){
      insert_box_into_box(objects[i]->box, this->box);
    }

    int longest_axis = 0;
    double max_distance = -std::numeric_limits<int>::infinity();

    for (int i = 1; i < 3; i++){
      double distance = this->box.max_corner(i) - this->box.min_corner(i);
      if (distance > max_distance){
        max_distance = distance;
        longest_axis = i;
      }
    }

    std::vector<std::shared_ptr<Object>> left, right;
    for (int i = 0; i < objects.size(); i++){
      if (objects[i]->box.center()(longest_axis) < ((box.max_corner(longest_axis) + box.min_corner(longest_axis)) / 2)){
        left.emplace_back(objects[i]);
      }
      else{
        right.emplace_back(objects[i]);
      }
    }

    if (right.empty() && left.size() != 0){
      right.emplace_back(left.back());
      left.pop_back();
    }
    else if (left.empty() && right.size() != 0){
      left.emplace_back(right.back());
      right.pop_back();
    }

    this->left = std::make_shared<AABBTree>(left, a_depth+1);
    this->right = std::make_shared<AABBTree>(right, a_depth+1);
    }
}
