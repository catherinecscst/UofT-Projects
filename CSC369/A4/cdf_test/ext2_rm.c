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
#include "utils.h"

unsigned char *disk;

int main(int argc, char **argv) {
    // This program takes two command line arguments.
    if (argc != 3) { 
        fprintf(stderr, "Usage: %s <image disk name> <absolute path to a file or link>\n", argv[0]);
        exit(1);
    }
    char *disk_name = argv[1]; // The first is the name of an ext2 formatted virtual disk.  *disk_image_path
    char *absolute_path = argv[2]; // The second is an absolute path on your ext2 formatted disk.  *target_path

    int abs_len = strlen(absolute_path);
    //check if the path is the root/directory -> fail
    if ((strcmp("/", absolute_path) == 0) || absolute_path[abs_len - 1] == '/') {
        fprintf(stderr, "Error: You cannot rm a directory.\n");
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

    int parent_inode_index = if_exist;

    struct ext2_inode *parent_inode;
    struct ext2_dir_entry *cur_entry;
    struct ext2_dir_entry *last_entry;
    parent_inode = (struct ext2_inode *)((void *)inode_table + sizeof(struct ext2_inode) * parent_inode_index);
    //接下去找child file inode index
    int if_target_index = -1;
    int num_blk = parent_inode->i_blocks / 2;
    int i, cur_size;
    bool if_stop = false;
    for(i = 0; ((i < num_blk) && (if_stop == false)); i++){
        cur_size = 0;
        while(cur_size < EXT2_BLOCK_SIZE){
            unsigned int cur_blk = parent_inode->i_block[i];
            cur_entry = (struct ext2_dir_entry *)(disk + EXT2_BLOCK_SIZE * cur_blk + cur_size);
            if ((cur_entry->file_type == (unsigned char)EXT2_FT_REG_FILE) || (cur_entry->file_type == (unsigned char)EXT2_FT_SYMLINK)){
                if ((strncmp(abs_child, cur_entry->name, cur_entry->name_len)==0) && (cur_entry->inode != 0)){
                    last_entry->rec_len += cur_entry->rec_len;
                    if_target_index = cur_entry->inode;
                    if_stop = true;
                    break;
                }
            }
            last_entry = (struct ext2_dir_entry *)(disk + EXT2_BLOCK_SIZE * cur_blk + cur_size);
            cur_size += cur_entry->rec_len;
        }
    }
    //if not FOUND
    if (if_target_index == -1){
        fprintf(stderr, "DOES NOT EXIST\n");
        exit(ENOENT); 
    }
    //printf("!CURSIZE:%d\n", cur_size);
    int prev_len;
    //找到做的事
    if(cur_size != 0){
        prev_len = cur_entry->rec_len;
        cur_entry = (void *)cur_entry - last_entry->rec_len;
        cur_entry->rec_len = prev_len + last_entry->rec_len;
    } else {
        prev_len = cur_entry->rec_len;
        int cur_size_update = cur_size + prev_len;
        void *source = (void *)cur_entry + prev_len;
        void *des = (void *)cur_entry;
        while(cur_size_update < EXT2_BLOCK_SIZE){
            last_entry->rec_len = cur_entry->rec_len;
            cur_size_update += cur_entry->rec_len;
            cur_entry = (void *)cur_entry + cur_entry->rec_len;
        }
        cur_entry = (void *)cur_entry - last_entry->rec_len;
        int need_size = EXT2_BLOCK_SIZE - prev_len;
        memcpy(des, source, need_size);
    }

    
    int newindex = if_target_index - 1;
    struct ext2_inode * target_inode = &inode_table[newindex];
    //update信息， 包括super block和group description
    target_inode->i_links_count--;
    sb->s_free_inodes_count ++;  
    gd->bg_free_inodes_count ++; 

    target_inode->i_dtime = (unsigned)time(NULL);
    update_bitmap(find_i_bitmap, newindex, 0); 

    int direct_bn;
    bool need_inderect = false;
    int num_blk_t = target_inode->i_blocks / 2;
    if(num_blk_t < 13){
        direct_bn = num_blk_t;
    } else if (num_blk_t > 12){
        direct_bn = 12;
        need_inderect = true;
    }
    //只有derect的情况
    for(i = 0; (i < direct_bn) && (target_inode->i_block[i]); i++){
        update_bitmap(find_b_bitmap, target_inode->i_block[i]-1, 0);
        gd->bg_free_blocks_count++;
        sb->s_free_blocks_count ++;
    }
    //need to do indirect, 超过范围
    if(need_inderect == true){
        unsigned int *blk_index = (void*)(disk + target_inode->i_block[12] * EXT2_BLOCK_SIZE);
        update_bitmap(find_b_bitmap, target_inode->i_block[12] - 1, 0);
        for (i = 12; i < num_blk_t; i++){
            int ib_index = *blk_index - 1;
            update_bitmap(find_b_bitmap, ib_index, 0);
            blk_index ++; 
            gd->bg_free_blocks_count++;
            sb->s_free_blocks_count ++;
        }
    }

    return 0;
}