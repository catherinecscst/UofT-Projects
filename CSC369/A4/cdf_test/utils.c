#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "utils.h"

#define TOTAL_INODES 32
#define TOTAL_BLOCKS 128

extern unsigned char* disk;

void split_path(char *abs_path, char *new_dir, char *parent_path){
    //printf("abs: %s\n", abs_path);
    char *path = abs_path;
    if((strlen(path) != 1) && (path[strlen(path) - 1] == '/')){
        path[strlen(path) - 1] = '\0';
    }
    int path_length = strlen(path);//  A/BB/C
    // printf("path:  %s\n", path);
    // printf("abs: %s\n", abs_path);
    int i = path_length - 1;       //  012345
    //printf("i: %d\n", i); 
    while (path[i] != '/'){
        i--;
    }
    strncpy(new_dir, path + i + 1, path_length - i);
    new_dir[path_length] = '\0';
    //printf("new_dir%s\n", new_dir);
    //printf("%d\n", i);
    if (i != 0) {
        strncpy(parent_path, path, i);
        parent_path[i] = '\0';
    }
    else if(i == 0){// /A/
        strncpy(parent_path, path, 2);
        parent_path[1] = '\0';
    }
}

int* get_bitmap(void *find, int total_size) {
  int* bitmap = malloc(sizeof(int) * total_size);
  char* byte;
  int i = 0;
  while(i < total_size){
    byte = find + (i / 8);
    bitmap[i] = (*byte >> (i % 8)) & 1;
    i++;
  }
  return bitmap;
}
//for restore
bool get_ibm_stga(unsigned int *blks, void *find_b_bitmap, int times){
    //unsigned char *b_bitmap = find_b_bitmap;
    int *byte;
    for (int i = 0; ((i < times) && (blks[i])); i++){
        byte = find_b_bitmap + ((blks[i] - 1)/(sizeof(char*)));
        //if its occupied already?
        if((*byte >> ((blks[i] - 1) % (sizeof(char*)))) & 1){
            return true;
        }
    }
    return false;
}

bool get_ibm_stagb(unsigned int *blks, void *find_b_bitmap, int ext){
    //unsigned char *b_bitmap = find_b_bitmap;
    int *byte;
    int if_is;
    if(blks[12]){
        byte = find_b_bitmap + ((blks[12] - 1)/(sizeof(char*)));
        if((*byte >> ((blks[12] - 1) % (sizeof(char*)))) & 1){
            unsigned int *new_index = (void *)(disk + blks[12] * EXT2_BLOCK_SIZE);
            if_is = get_ibm_stga(new_index, find_b_bitmap, ext);
            if(if_is == true){
                return true;
            }
        }
    }
    return false;
}

void update_bitmap(void* find, int ib_index, int s) {
  char* byte = find + (ib_index / 8);
  *byte = (*byte & ~(1 << (ib_index % 8))) | (s << (ib_index % 8));
}

int get_inode_index(int* i_bitmap){
    ///============================> inode index
    int j = 0;
    while ((j < TOTAL_INODES) && (i_bitmap[j] != 0)){
        j++;
    }
    int if_free_inode = j;
    return if_free_inode;
}

int get_blocks(int* b_bitmap){
    ///============================> blk index
    int j = 0;
    while ((j < TOTAL_INODES) && (b_bitmap[j] != 0)){
        j++;
    }
    int if_free_blk = j;
    return if_free_blk;
}

int set_size(int length){
    int result;
    if (length % 4 != 0){
        result = 12 + 4 * (length / 4);
    } else{
        result = 12 + length;
    }
    return result;
}

int check_dir_exist(char *path, struct ext2_inode *inode_table){
    unsigned int if_exist;
    int count, cur_size, is_dir, same, cur_blk;

    char copy[512];
    strcpy(copy, path);
    copy[strlen(path) + 1] = '\0';
        
    // make the parent inode point to the root
    struct ext2_inode *cur_inode = &inode_table[EXT2_ROOT_INO - 1];
    if ((copy[0] == '/') && (strlen(path) == 1)){
        return 1;
    }
    else if (strlen(path) != 1) {
        char* nxt = strtok(copy, "/");
        while (nxt != NULL){
            struct ext2_dir_entry *actual_dir;
            count = 0;
            is_dir = 0;
            same = 0;
            if_exist = 0;
           
            // loop every block
            while (count < 12 && if_exist == 0){
                if (cur_inode->i_block[count] != 0){
                    cur_size = 0;
                    cur_blk = cur_inode->i_block[count];
                    actual_dir = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * cur_blk);
                    while(cur_size < EXT2_BLOCK_SIZE){
                        if ((strlen(nxt) == actual_dir->name_len) && (strncmp(nxt, actual_dir->name, strlen(nxt)) == 0)){
                            is_dir = 1;
                        }
                        if (EXT2_FT_DIR & actual_dir->file_type){
                            same = 1;
                        }
                        if ((is_dir == 1) && (same == 1)){
                            if_exist = actual_dir->inode;
                            break;
                        }
                        else{
                            cur_size += actual_dir->rec_len;
                            actual_dir = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * cur_blk + cur_size);

                        }
                        is_dir = 0;
                        same = 0;
                    }
                }
                count ++;
            }
            if (if_exist == 0){
                return -1;
            }
            cur_inode = &inode_table[if_exist-1];
            nxt = strtok(NULL, "/");
        }
    }
    return if_exist - 1;
}

int check_child(struct ext2_inode *parent_inode, struct ext2_inode *inode_table, char *abs_child){
    int index; //loop over block
    int cur_blk;
    struct ext2_dir_entry *cur_dir;
    for (index = 0; index < parent_inode->i_blocks/2; index++){
        //printf("parent_inode->i_blocks/2: %d",parent_inode->i_blocks/2);
        int cur_size = 0;
        int is_dir = 1;
        int same = 0;

        cur_blk = parent_inode->i_block[index];
        cur_dir = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * cur_blk);
        while (cur_size < EXT2_BLOCK_SIZE){
            cur_size += cur_dir->rec_len;
            //printf("curent name !!!!!!%s\n", cur_dir->name);
            //printf("curent length !!!!!!%d\n", cur_dir->name_len);
            if (cur_dir->file_type != EXT2_FT_DIR){
                is_dir = 0;
            }
            if ((cur_dir->name_len == strlen(abs_child)) && (strncmp(abs_child, cur_dir->name, strlen(abs_child)) == 0)){
                same = 1;
            }
            if (is_dir == 0 && same == 1){
                return -1;
            }
            cur_dir = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * cur_blk + cur_size);
        }

    }
    return 0;
}

int find_dir_entry(struct ext2_inode *parent_inode, char* abs_child, void *find_i_bitmap){
    struct ext2_dir_entry *parent_entry;
    int num_blk = parent_inode->i_blocks / 2;
    
    int i, cur_size, size_sett, inode_tor;
    for (i = 0; i < num_blk; i++){
        cur_size = 0;
        while (cur_size < EXT2_BLOCK_SIZE){
            //printf("HERE CUR_SIZE:%d\n", cur_size);
            unsigned int ind_blk = parent_inode->i_block[i];
            parent_entry = (struct ext2_dir_entry *)(disk + EXT2_BLOCK_SIZE * ind_blk + cur_size);
            size_sett = set_size(strlen(parent_entry->name));

            int prev_size = cur_size;
            cur_size += parent_entry->rec_len;

            if(size_sett != parent_entry->rec_len){
                int bg; 
                int fi = prev_size + parent_entry->rec_len;
                //寻找任何同名文件
                for (bg = prev_size + size_sett;  bg < fi + 1; bg += 4){
                    struct ext2_dir_entry * child_entry = (struct ext2_dir_entry *)(disk + EXT2_BLOCK_SIZE * ind_blk + bg);
                    if ((child_entry->file_type == (unsigned char)EXT2_FT_REG_FILE) || 
                        (child_entry->file_type == (unsigned char)EXT2_FT_SYMLINK)) {
                        if((child_entry->inode != 0) && (strncmp(abs_child, child_entry->name, child_entry->name_len) == 0)){
                            inode_tor = child_entry->inode;
                            int irm = (inode_tor-1) % (sizeof(char*));
                            unsigned char *pt = find_i_bitmap;
                            int blk_spot = pt[(inode_tor - 1)/sizeof(char*)];

                            if(!((blk_spot >> (irm)) & 1)){
                                parent_entry->rec_len = bg - prev_size;
                                return child_entry->inode;
                            } else {
                                return -1; 
                            }
                        }
                    }
                }       
            }
        }
    }   
    return -1;
}