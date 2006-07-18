#include<stdlib.h>
#include<stdio.h>

struct tree_el {
   int key;
   struct tree_el * right, * left;
};

typedef struct tree_el node;

void insert(node ** tree, node * item) {
   if(!(*tree)) {
      *tree = item;
      return;
   }
   if(item->key<(*tree)->key) {
      printf("inserting left %d \n",item->key);
      printf("root is %d \n",(*tree)->key);
      insert(&(*tree)->left, item);
      
   } else if(item->key>(*tree)->key) {
      printf("inserting right %d \n",item->key);
      printf("root is %d \n",(*tree)->key);
      insert(&(*tree)->right, item);
   }   
}

void printout(node * tree) {
   if(tree->left) printout(tree->left);
   printf("%d\n",tree->key);
   if(tree->right) printout(tree->right);
}

int main() {
   node * curr, * root;
   long i;

   root = NULL;
// number of nodes in a balanced binary tree is of the form 2^n - 1
// e.g 31, 63, 127, 255, 511, 1023, 2047, 4094, 8191 ...

   for(i=1;i<=4;i++) {
      curr = (node *)malloc(sizeof(node));
      curr->left = curr->right = NULL;
      curr->key = rand();
      insert(&root, curr);
   }
   //printf("root is %d \n",root->key);
   //printf("inserted \n");
   //printout(root);
}


