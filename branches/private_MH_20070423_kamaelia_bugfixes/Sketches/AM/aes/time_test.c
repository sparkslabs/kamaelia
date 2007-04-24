#include <sys/time.h>
#include <stdio.h>

int main() {
	struct timeval tp;
	gettimeofday(&tp, NULL);
	printf("%d",tp.tv_usec);
}
