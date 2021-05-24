#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include "utils.h"

unsigned char *disk;


int main(int argc, char **argv) {
    // This program takes two command line arguments.
    if (argc != 3) { 
        fprintf(stderr, "Usage: %s <image disk name> <absolute path on ext2 image>\n", argv[0]);
        exit(1);
    }
    //check if the path is the root -> fail
    if (strcmp("/", argv[2]) == 0) {
        printf("Error: You cannot make the root directory, as the root directory already exists.\n");
        exit(EEXIST);
    } 

    char *disk_name = argv[1]; // The first is the name of an ext2 formatted virtual disk.  *disk_image_path
    char *absolute_path = argv[2]; // The second is an absolute path on your ext2 formatted disk.  *target_path
    
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
    struct ext2_group_desc *gd = (struct ext2_group_desc *) ((void *)disk + 2 * EXT2_BLOCK_SIZE); //get group description.
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
        fprintf(stderr, "Error: <%s> This directory already exist!\n", absolute_path);
        exit(EEXIST);
    }

    // printf("Confirmed absolute_path is not exist 22222222\n");
    // printf("Absolute Path: %s\n", absolute_path);
    char abs_child[512];
    char abs_parent[512];
    split_path(absolute_path, abs_child, abs_parent);
    int child_name_len = strlen(abs_child);
    
    // printf("Before checking parent_path if not exist 2222222222\n");
    if_exist = check_dir_exist(abs_parent, inode_table);
    // printf("After checking parent_path if not exist 22222222222\n");
    if (if_exist == -1){ //parent path invalid
        fprintf(stderr, "Error: <%s> This parent directory does not exist!\n", abs_parent);
        exit(ENOENT);
    }
    int parent_inode_index = if_exist;
    struct ext2_inode *parent_inode = (struct ext2_inode *)((void *)inode_table + sizeof(struct ext2_inode) * parent_inode_index);
    // printf("Confirmed parent_path does exist 333333333333\n");
    // printf("Parent Path: %s\n", abs_parent);
    // printf("Child Name: %s\n", abs_child);

    //Check if a file have the same name with the directory to be make exists
    int if_name = check_child(parent_inode, inode_table, abs_child);
    if (if_name == -1){
        fprintf(stderr, "A file have the same name with the directory to be make exists\n");
        exit(EEXIST);
    }
    // printf("!!!!!!!!!!!!%d", if_name);

    // printf("Same file does not exit! -- Confirmed!\n");
    int* i_bitmap = get_bitmap(find_i_bitmap, TOTAL_INODES);
    int* b_bitmap = get_bitmap(find_b_bitmap, TOTAL_BLOCKS);
    //=======> Find free inode
    int find_inode = get_inode_index(i_bitmap);
    if (find_inode == TOTAL_INODES) {
        fprintf(stderr, "Can not find any free inodes!\n");
        exit(ENOSPC);
    } else {
        gd->bg_free_inodes_count --;
        sb->s_free_inodes_count --;
    }
    // printf("Find free inode: %d\n", find_inode);
    //=======> Find free blocks
    int find_blocks = get_blocks(b_bitmap);
    if (find_blocks == TOTAL_BLOCKS){
        fprintf(stderr, "Can not find any free blocks!\n");
        exit(ENOSPC);
    } else {
        gd->bg_free_blocks_count --;
        sb->s_free_blocks_count --;
    }
    //===========================================================
    //找block space！！
    struct ext2_dir_entry *dir;
    int if_space = -1;
    int s, size_checker, loop_blocks, min_size;
    for (s = 0; (s < ((parent_inode->i_blocks / 2)) && (if_space == -1)); s++) {
        loop_blocks = parent_inode->i_block[s];
        dir = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * loop_blocks);
        size_checker = 0;
        while (size_checker < EXT2_BLOCK_SIZE) {
            size_checker += dir->rec_len;
            if (size_checker == EXT2_BLOCK_SIZE){
                min_size = set_size(child_name_len) + set_size(dir->name_len);
                if(!(dir->rec_len < min_size)){
                    if_space = 0;
                    int prev_reclen = dir->rec_len;
                    dir->rec_len = set_size(dir->name_len);
                    dir = (void*)dir + set_size(dir->name_len);
                    dir->inode = find_inode + 1;
                    dir->rec_len = prev_reclen - set_size(dir->name_len);
                    dir->name_len = child_name_len;
                    dir->file_type = EXT2_FT_DIR;
                    strncpy((void*)dir + 8, abs_child, child_name_len);
                    break;
                }
            }
            dir = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * loop_blocks + size_checker);
        }
    }
    if (if_space == -1) {
        // reserve one more for potential extending a block for dir
        b_bitmap = get_bitmap(find_b_bitmap, TOTAL_BLOCKS);
        int free_block = get_blocks(b_bitmap);
        if (find_blocks == TOTAL_BLOCKS){
            fprintf(stderr, "Can not find any free blocks!\n");
            exit(ENOSPC);
        } else {
            gd->bg_free_blocks_count --;
        }
        // printf("=======start to create dir=======\n");
        dir = (void*)disk + EXT2_BLOCK_SIZE * (free_block + 1);
        dir->inode = find_inode + 1;
        dir->rec_len = EXT2_BLOCK_SIZE;
        dir->name_len = child_name_len; 
        dir->file_type = EXT2_FT_DIR;
        strncpy((void*)dir + 8, abs_child, child_name_len);
        // update block bitmap
        update_bitmap(find_b_bitmap, free_block, 1);
        // update parent dir inode
        parent_inode->i_size += EXT2_BLOCK_SIZE;
        parent_inode->i_blocks += 2;
        parent_inode->i_block[(parent_inode->i_size / EXT2_BLOCK_SIZE)] = free_block + 1;

    }

    //printf("Find free blocks: %d\n", find_blocks);
    struct ext2_dir_entry *dir_base = (struct ext2_dir_entry *)((void *)disk + EXT2_BLOCK_SIZE * (find_blocks + 1));
    // .  curent directory
    dir_base->name[0] = '.';
    dir_base->name[1] = '\0';
    dir_base->name_len = 1;
    dir_base->inode = find_inode + 1;
    dir_base->file_type = EXT2_FT_DIR;
    dir_base->rec_len = 12;
    
    // .. parent directory
    unsigned short cur_reclen = dir_base->rec_len;
    dir_base = (struct ext2_dir_entry *)((void*)dir_base + dir_base->rec_len);
    dir_base->name[0] = '.';
    dir_base->name[1] = '.';
    dir_base->name[2] = '\0';
    dir_base->name_len = 2;
    dir_base->inode = parent_inode_index + 1;
    dir_base->file_type = EXT2_FT_DIR;
    dir_base->rec_len = EXT2_BLOCK_SIZE - cur_reclen;
    update_bitmap(find_b_bitmap, find_blocks, 1);
    //printf("FINISHED . AND ..\n");

    // create an inode for the new dir
    struct ext2_inode *newdir_inode = (struct ext2_inode *)((void *)inode_table + sizeof(struct ext2_inode) * find_inode);
    newdir_inode->i_mode = EXT2_S_IFDIR;
    newdir_inode->i_size = EXT2_BLOCK_SIZE;
    newdir_inode->i_links_count = 2;
    newdir_inode->i_blocks = 2;
    newdir_inode->i_block[0] = find_blocks + 1;
    parent_inode->i_links_count++; 
    update_bitmap(find_i_bitmap, find_inode, 1);
    //printf("FINISHED new dir inode\n");
    
    gd->bg_used_dirs_count++;
  
  return 0;
}
