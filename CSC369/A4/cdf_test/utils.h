#include "ext2.h"

#define TOTAL_INODES 32
#define TOTAL_BLOCKS 128
#define MAX_I_BLOCKS 13

void split_path(char *abs_path, char *new_dir, char *parent_path);

int get_inode_index(int* i_bitmap);
int get_blocks(int* b_bitmap);

int check_dir_exist(char *path, struct ext2_inode *inode_table);
int check_child(struct ext2_inode *parent_inode, struct ext2_inode *inode_table, char *abs_child);
int* get_bitmap(void *find, int total_size);
bool get_ibm_stga(unsigned int *blks, void *find_b_bitmap, int times);
bool get_ibm_stagb(unsigned int *blks, void *find_b_bitmap, int ext);

void update_bitmap(void* find, int ib_index, int s);
int set_size(int length);
int find_dir_entry(struct ext2_inode *parent_inode, char* abs_child, void *find_i_bitmap);
