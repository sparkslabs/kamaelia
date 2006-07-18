# include <stdio.h>


void createTree(int no);
int getKey(int id); 
int arr[16];

void createTree(int no) {
// since it is a complete tree we can create it as an array
    int i;
    for(i=0; i<no; i++) {
       arr[i] = i+1;
    }
	
}

int getKey(int id) {
// given the id of the node return the key at that node.
// extract each digit and decide left or right child if it is 0 or 1 resply.
    int op;
    int index = 0;
    
    while(id != 1) {
       op = id % 10;
       id = id/10;
       printf("op = %d \n",op);
       printf("id = %d \n",id);
       if(op == 0) {
	  index = index * 2+ 1; // left child
          printf("index is %d \n",index);
       } else if(op == 1) {
	  index = index * 2 + 2; //right child
          printf("index is %d \n",index);
       }else {
	 printf("invalid id %d",id);
       }
    }
    printf("index is %d \n",index);
    printf("arr[index] is %d \n",arr[index]);
    return arr[index];	
}


int main() {
	int id = 1110;
	int key;
	createTree(16);
	
	key = getKey(id);
	printf("key for id %d",id);
	printf("is %d",key);
}
