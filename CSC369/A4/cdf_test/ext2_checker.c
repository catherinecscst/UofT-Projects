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
	// This program takes one command line arguments.
    if (argc != 2) { 
        fprintf(stderr, "Usage: %s <image disk name> \n", argv[0]);
        exit(1);
    }
    char *disk_name = argv[1];
    int fd = open(disk_name, O_RDWR);

    disk = mmap(NULL, TOTAL_BLOCKS * EXT2_BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (disk == MAP_FAILED) {
        fprintf(stderr, "Error: mmap - Could not open disk image");
        exit(1);
    }
    
	return 0;
}
