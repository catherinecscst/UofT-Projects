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
    // This program takes 3 command line arguments.
    if (argc != 4) { 
        fprintf(stderr, "Usage: %s <image disk name> <absolute path source> <absolute path destination>\n", argv[0]);
        exit(1);
    }
    char *disk_name = argv[1]; 
    char *src_abs = argv[2]; 
    char *dest_abs = argv[3];
    
    if (src_abs[0] != '/') {
        fprintf(stderr, "Error: <%s> is not an absolute path." , src_abs);
        exit(EINVAL);
    }
    if (dest_abs[0] != '/') {
        fprintf(stderr, "Error: <%s> is not an absolute path." , src_abs);
        exit(EINVAL);
    }
    // Checking if the source path is valid.
    struct stat s;
	if (lstat(src_abs, &s) == -1) {
		fprintf(stderr, "Invalid target path!\n");
		return ENOENT;
	}
    
    int fd = open(disk_name, O_RDWR);

    disk = mmap(NULL, TOTAL_BLOCKS * EXT2_BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (disk == MAP_FAILED) {
        fprintf(stderr, "Error: mmap - Could not open disk image");
        exit(1);
    }


	return 0;
}
