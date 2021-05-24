#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include "ext2.h"
#include "utils.h"

unsigned char *disk;

int main(int argc, char **argv) {
	// This program takes two command line arguments.
    if (argc != 3) { 
        fprintf(stderr, "Usage: %s <image disk name> <absolute path to a file or link >\n", argv[0]);
        exit(1);
    }
    char *disk_name = argv[1]; // The first is the name of an ext2 formatted virtual disk.  *disk_image_path
    char *absolute_path = argv[2]; // The second is an absolute path on your ext2 formatted disk.  *target_path
    
    int abs_len = strlen(absolute_path);
    //check if the path is the root/directory -> fail
    if ((strcmp("/", absolute_path) == 0) || absolute_path[abs_len - 1] == '/') {
        fprintf(stderr, "Error: You cannot restore a directory.\n");
        exit(EISDIR);
    }
        //check if the target path is absolute
    if (absolute_path[0] != '/') {
        fprintf(stderr, "Error: <%s> is not an absolute path." , absolute_path);
        exit(EINVAL);
    }

    int fd = open(disk_name, O_RDWR);

    disk = mmap(NULL, TOTAL_BLOCKS * EXT2_BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (disk == MAP_FAILED) {
        fprintf(stderr, "Error: mmap - Could not open disk image");
        exit(1);
    }

    struct ext2_super_block *sb = (struct ext2_super_block *)((void *)disk + EXT2_BLOCK_SIZE);
    //Group desciptor
    struct ext2_group_desc* gd = (struct ext2_group_desc *) ((void *)disk + 2 * EXT2_BLOCK_SIZE); //get group description.
    //Inode table. consists of Inode.
    struct ext2_inode *inode_table = (struct ext2_inode *)(disk + EXT2_BLOCK_SIZE * gd->bg_inode_table);
    void *find_i_bitmap = disk + EXT2_BLOCK_SIZE * gd->bg_inode_bitmap;
    void *find_b_bitmap = disk + EXT2_BLOCK_SIZE * gd->bg_block_bitmap;

    // printf("Before checking absolute_path if not exist 111111\n");
    char copy_path[512];
    strncpy(copy_path, absolute_path, strlen(absolute_path));
    copy_path[strlen(absolute_path) + 1] = '\0';

    int if_exist = check_dir_exist(copy_path, inode_table);
    // printf("After checking absolute_path if not exist 111111\n");
    if (if_exist != -1){ //absolute path = dir already exist
        fprintf(stderr, "Error: You cannot rm a directory!\n");
        exit(EISDIR);
    }

    char abs_child[512];
    char abs_parent[512];
    split_path(absolute_path, abs_child, abs_parent);
    //int child_name_len = strlen(abs_child);

    if_exist = check_dir_exist(abs_parent, inode_table);
    // printf("After checking parent_path if not exist 22222222222\n");
    if (if_exist == -1){ //parent path invalid
        fprintf(stderr, "Error: <%s> This parent directory does not exist!\n", abs_parent);
        exit(ENOENT);
    }
    //recieved parent inode index;
    int parent_inode_index = if_exist;
    struct ext2_inode *parent_inode;
    parent_inode = (struct ext2_inode *)((void *)inode_table + sizeof(struct ext2_inode) * parent_inode_index);

    //找到dir entry才能进行restore
    int if_restore_idx = find_dir_entry(parent_inode, abs_child, find_i_bitmap);
    if (if_restore_idx == -1){
	 		printf("Error: This file is already exist!\n");
	 		exit(EEXIST);	
	}

	int newindex = if_restore_idx - 1;
    struct ext2_inode* restored_inode = &inode_table[if_restore_idx - 1];
    restored_inode->i_links_count++;
	sb->s_free_inodes_count--;  
    gd->bg_free_inodes_count--;
    update_bitmap(find_i_bitmap, newindex, 1);


    unsigned int *blks = restored_inode->i_block;
    int num_blk = restored_inode->i_blocks / 2;
    //get_bitmap 不能用 要make a new one to check!!!!
    bool satisfy_direct = get_ibm_stga(blks, find_b_bitmap, 12);
    bool satisfy_indirect = get_ibm_stga(blks, find_b_bitmap, num_blk);
    
    int idx, i;
    if(satisfy_direct && satisfy_indirect){
    	//need to do both direct and inderect
    	for(i = 0; (i < 12) && (blks[i]); i++){
    		idx = blks[i] - 1;
   			update_bitmap(find_b_bitmap, idx, 1);
    	}
    	if((i == 12) && (blks[i])){
    		update_bitmap(find_b_bitmap, blks[i] - 1, 1);
    		unsigned int *new_bi = (void *)disk + EXT2_BLOCK_SIZE * blks[12];
    		int inderect_num = num_blk - 13;
    		for(i = 0; i < inderect_num; i++){
    			update_bitmap(find_b_bitmap, *new_bi - 1, 1);
    			gd->bg_free_blocks_count--;
    			sb->s_free_blocks_count--;
    			new_bi++;
    		}
    	}
    	gd->bg_free_blocks_count--;
    	sb->s_free_blocks_count--;

    } else {
    	//只用有的
    	for(i = 0; i < MAX_I_BLOCKS; i++){
    		int free_block_index = get_blocks(find_b_bitmap);
    		if (free_block_index == TOTAL_BLOCKS){
	        	fprintf(stderr, "Can not find any free blocks!\n");
	        	exit(ENOSPC);
    		} else {
        		gd->bg_free_blocks_count--;
        		sb->s_free_blocks_count--;
    		}
    		blks[i] = free_block_index;
    		update_bitmap(find_b_bitmap, free_block_index - 1, 1);
    	}
    }
	return 0;
}
