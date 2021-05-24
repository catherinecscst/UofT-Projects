#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include "ext2.h"

unsigned char *disk;


int main(int argc, char **argv) {

    if(argc != 2) {
        fprintf(stderr, "Usage: %s <image file name>\n", argv[0]);
        exit(1);
    }
    int fd = open(argv[1], O_RDWR);

    disk = mmap(NULL, 128 * 1024, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if(disk == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    struct ext2_super_block *sb = (struct ext2_super_block *)(disk + 1024);
    printf("Inodes: %d\n", sb->s_inodes_count);
    printf("Blocks: %d\n", sb->s_blocks_count);

    struct ext2_group_desc *gd = (struct ext2_group_desc *)(disk + 2048);
    printf("Block group:\n");
    printf("    block bitmap: %d\n", gd->bg_block_bitmap);
    printf("    inode bitmap: %d\n", gd->bg_inode_bitmap);
    printf("    inode table: %d\n", gd->bg_inode_table);
    printf("    free blocks: %d\n", gd->bg_free_blocks_count);
    printf("    free inodes: %d\n", gd->bg_free_inodes_count);
    printf("    used_dirs: %d\n", gd->bg_used_dirs_count);
    
    //============== EX 9 FOLLOWING ============================================
    int i, j;
    int* dir = malloc(sizeof(int) * sb->s_inodes_count);
    memset(dir, 0, sizeof(int) * sb->s_inodes_count);
    unsigned char* bitmap = (unsigned char *) (disk + EXT2_BLOCK_SIZE * gd->bg_block_bitmap);
    unsigned char temp;
    printf("Block bitmap: ");
    for(i = 0; i < sb->s_blocks_count / 8; i++){
        printf(" ");
        for(j = 0; j < 8; j++){
            temp = *bitmap;
            printf("%d", (temp >> j) & 0x1);
        }
        bitmap++;

    }
    printf("\n");

    bitmap = (disk + EXT2_BLOCK_SIZE * gd->bg_inode_bitmap);
    printf("Inode bitmap: ");
    for(i = 0; i < sb->s_blocks_count / 32; i++){
        printf(" ");
        for(j = 0; j < 8; j++){
            temp = *bitmap;
            printf("%d", (temp >> j) & 0x1);
        }
        bitmap++;

    }
    printf("\n");

    printf("\nInodes:\n");
    
    char* indt = (char *)(disk + EXT2_BLOCK_SIZE * gd->bg_inode_table);
    char type = 'O';
    int dirnum = 0;

    struct ext2_inode *ind;
    for (i = EXT2_ROOT_INO - 1; i < sb->s_inodes_count; i++){
        if (!(i < EXT2_GOOD_OLD_FIRST_INO && i != EXT2_ROOT_INO - 1)) {
            ind = (struct ext2_inode *)(indt + sizeof(struct ext2_inode) * i);
            if (ind->i_size != 0) { 
                if (ind->i_mode & EXT2_S_IFREG) {
                    type = 'f';
                } else if (ind->i_mode & EXT2_S_IFDIR) {
                    type = 'd';
                    dir[i] = 1;
                    dirnum++;
                }
                printf("[%d] type: %c size: %d links: %d blocks: %d\n", 
                    i + 1, type, ind->i_size, ind->i_links_count, ind->i_blocks);

                j = 0;
                int bn = ind->i_blocks / 2;
                if (bn <= 12){
                    while(j < bn){
                        printf("[%d] Blocks:  %d\n", i + 1, ind->i_block[j]); 
                            j++;
                        }
                    } else {
                        for (j = 0; j < 12; j++) {
                            printf("[%d] Blocks:  %d\n", i + 1, ind->i_block[j]);
                        }
                    }
            }
        }
    }
    //============== EX 9 FOLLOWING ============================================
    printf("\n"); 
    printf("Directory Blocks:\n");
    struct ext2_dir_entry* de;
    int k, m;
    char * name;
    for (i = EXT2_ROOT_INO - 1; i < sb->s_inodes_count; i++) {
        if (dir[i] == 1){
            ind = (struct ext2_inode*)(indt + sizeof(struct ext2_inode) * i);            
            for (j = 0; j < ind->i_blocks / 2; j++) {

                printf("   DIR BLOCK NUM: %d (for inode %d)\n", ind->i_block[j], i + 1);
                de = (struct ext2_dir_entry*)(disk + EXT2_BLOCK_SIZE * ind->i_block[j]);

                m = 0;
                while (m < EXT2_BLOCK_SIZE ){
                    m += de->rec_len;
                    printf("Inode: %d ", de->inode);
                    printf("rec_len: %d ", de->rec_len);
                    printf("name_len: %d ", de->name_len); 
                    name = malloc(de->name_len);                   

                    if (de->file_type & EXT2_FT_REG_FILE) {
                        printf("type= f ");
                    } else if (de->file_type & EXT2_FT_DIR) {
                        printf("type= d ");
                    }

                    for (k = 0; k < de->name_len; k++) {
                      name[k] = de->name[k];
                    }
                    printf("name=%s\n", name);
                    de = (void *) de + de->rec_len;
                }
            }

        }
    }

}