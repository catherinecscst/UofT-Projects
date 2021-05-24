all : ext2_mkdir ext2_rm ext2_restore ext2_checker ext2_ln read

ext2_mkdir : ext2_mkdir.o utils.o
	gcc -Wall -Werror -g -o ext2_mkdir ext2_mkdir.o utils.o

ext2_rm : ext2_rm.o utils.o
	gcc -Wall -Werror -g -o ext2_rm ext2_rm.o utils.o

ext2_restore : ext2_restore.o utils.o
	gcc -Wall -Werror -g -o ext2_restore ext2_restore.o utils.o

ext2_checker: ext2_checker.o utils.o
	gcc -Wall -Werror -g -o ext2_checker ext2_checker.o utils.o

ext2_ln: ext2_ln.o utils.o
	gcc -Wall -Werror -g -o ext2_ln ext2_ln.o utils.o

read : readimage.o utils.o
	gcc -Wall -Werror -g -o read readimage.o utils.o

%.o : %.c
	gcc -Wall -g -c $<

clean:
	rm -f ext2_mkdir ext2_rm ext2_restore ext2_checker ext2_ln read *.o *~
