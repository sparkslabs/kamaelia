#include <stdlib.h>
#include <stdio.h>


unsigned long *tree;
unsigned long num_users;

unsigned int get_depth(unsigned long count) {
	unsigned long l = count;
	unsigned int depth = 0;

	while((l >>= 1) != 0) {
		depth++;
	}
	//more than one 1s in the binary representation
	if( (count & (count -1)) != 0) depth += 1;

	return depth;
}

void build_tree(unsigned long count) {
	unsigned long l;
	num_users = count;
	tree = (unsigned long *)malloc(2 * count * sizeof(unsigned long));
	tree[0] = 0; //not used
	//the root starts from index 1
	unsigned long num_elements = 2 * count;
	for ( l = 1; l < num_elements; l++) {
		tree[l] = l;
	}
}


void print_keys(unsigned long user_id) {
	printf("user key: %u\n", tree[user_id]);
	while( (user_id = user_id / 2) != 0) {
		printf("%u\n", tree[user_id]);
	}
}



//todo
void get_common_keys(unsigned long keys[], unsigned long ids[], unsigned long count) {
	
}


int main(int argc, char* argv[])
{
        int i;
	build_tree(8);
	print_keys(15);
	print_keys(8);
	printf("depth=%u\n", get_depth(8));
	printf("depth=%u\n", get_depth(5));
	printf("depth=%u\n", get_depth(4));

	return 0;
}
