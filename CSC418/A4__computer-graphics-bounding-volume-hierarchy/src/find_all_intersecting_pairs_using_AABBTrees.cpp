#include "find_all_intersecting_pairs_using_AABBTrees.h"
#include "box_box_intersect.h"
// Hint: use a list as a queue
#include <list> 

void find_all_intersecting_pairs_using_AABBTrees(
  const std::shared_ptr<AABBTree> & rootA,
  const std::shared_ptr<AABBTree> & rootB,
  std::vector<std::pair<std::shared_ptr<Object>,std::shared_ptr<Object> > > & 
    leaf_pairs)
{
  
  // Find all intersecting pairs of leaf boxes between one AABB tree and another.

  std::list<std::pair<std::shared_ptr<AABBTree>, std::shared_ptr<AABBTree>>> q;
  if (box_box_intersect(rootA->box, rootB->box)){
    q.emplace_front(rootA, rootB);
  }
  std::shared_ptr<AABBTree> node_A, node_B;

  while (!q.empty()){
    node_A = q.back().first;
    node_B = q.back().second;
    q.pop_back();

    if (node_A->num_leaves <= 2 && node_B->num_leaves <= 2){
      if ((node_A->left && node_B->left) && box_box_intersect(node_A->left->box, node_B->left->box)){
        leaf_pairs.emplace_back(node_A->left, node_B->left);
      }
      if ((node_A->left && node_B->right) && box_box_intersect(node_A->left->box, node_B->right->box)){
        leaf_pairs.emplace_back(node_A->left, node_B->right);
      }
      if ((node_A->right && node_B->left) && box_box_intersect(node_A->right->box, node_B->left->box)){
        leaf_pairs.emplace_back(node_A->right, node_B->left);
      }
      if ((node_A->right && node_B->right) && box_box_intersect(node_A->right->box, node_B->right->box)){
        leaf_pairs.emplace_back(node_A->right, node_B->right);
      }
    }
    else if (node_A->num_leaves <= 2){
      if (box_box_intersect(node_A->box, node_B->left->box)){
        q.emplace_front(node_A, std::static_pointer_cast<AABBTree>(node_B->left));
      }
      if (box_box_intersect(node_A->box, node_B->right->box)){
        q.emplace_front(node_A, std::static_pointer_cast<AABBTree>(node_B->right));
      }
    }
    else if (node_B->num_leaves <= 2){
      if (box_box_intersect(node_B->box, node_A->left->box)){
        q.emplace_front(std::static_pointer_cast<AABBTree>(node_A->left), node_B);
      }
      if (box_box_intersect(node_B->box, node_A->right->box)){
        q.emplace_front(std::static_pointer_cast<AABBTree>(node_A->right), node_B);
      }
    }
    else{
      if (box_box_intersect(node_A->left->box, node_B->left->box)){
        q.emplace_front(std::static_pointer_cast<AABBTree>(node_A->left), std::static_pointer_cast<AABBTree>(node_B->left));
      }
      if (box_box_intersect(node_A->left->box, node_B->right->box)){
        q.emplace_front(std::static_pointer_cast<AABBTree>(node_A->left), std::static_pointer_cast<AABBTree>(node_B->right));
      }
      if (box_box_intersect(node_A->right->box, node_B->left->box)){
        q.emplace_front(std::static_pointer_cast<AABBTree>(node_A->right), std::static_pointer_cast<AABBTree>(node_B->left));
      }
      if (box_box_intersect(node_A->right->box, node_B->right->box)){
        q.emplace_front(std::static_pointer_cast<AABBTree>(node_A->right), std::static_pointer_cast<AABBTree>(node_B->right));
      }
    }
  }

}
