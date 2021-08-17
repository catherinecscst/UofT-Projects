#include "point_AABBTree_squared_distance.h"
#include <queue> // std::priority_queue

bool point_AABBTree_squared_distance(
    const Eigen::RowVector3d & query,
    const std::shared_ptr<AABBTree> & root,
    const double min_sqrd,
    const double max_sqrd,
    double & sqrd,
    std::shared_ptr<Object> & descendant)
{
  
  // Compute the distrance from a query point to the objects stored in a AABBTree using a priority queue. 
  // Note: this function is not meant to be called recursively.


  auto cmp = [](std::pair<double, std::shared_ptr<AABBTree>> n1, std::pair<double, std::shared_ptr<AABBTree>> n2)
  {return n1.first > n2.first;};
  std::priority_queue<std::pair<double, std::shared_ptr<AABBTree>>, std::vector<std::pair<double, std::shared_ptr<AABBTree>>>, decltype(cmp)> q(cmp);

  double curr_distance, distance;
  double min_distance = std::numeric_limits<double>::infinity();
  std::shared_ptr<Object> curr_descendant;
  q.emplace(point_box_squared_distance(query, root->box), root);
  std::shared_ptr<AABBTree> node;
  
  while (!q.empty()){
    distance = q.top().first;
    node = q.top().second;
    q.pop();

    if (distance < min_distance){
      if (node->num_leaves <= 2){

        if (node->left){
          if (node->left->point_squared_distance(query, min_sqrd, max_sqrd, curr_distance, curr_descendant)){
            if (curr_distance < min_distance){
              min_distance = curr_distance;
              descendant = node->left;
            }
          }
        }
        if (node->right){
          if (node->right->point_squared_distance(query, min_sqrd, max_sqrd, curr_distance, curr_descendant)) {
            if (curr_distance < min_distance){
              min_distance = curr_distance;
              descendant = node->right;
            }
          }
        }
      }
      else{
        q.emplace(point_box_squared_distance(query, node->left->box), std::static_pointer_cast<AABBTree>(node->left));
        q.emplace(point_box_squared_distance(query, node->right->box), std::static_pointer_cast<AABBTree>(node->right));
      }
    }
  }

  sqrd = min_distance;

  if (descendant){
    return true;
  }
  return false;

}
