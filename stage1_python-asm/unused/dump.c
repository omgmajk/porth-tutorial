#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

void dump(uint64_t x) {
	char buf[32]; // Stack buffer
	size_t buf_sz = 1;
	buf[sizeof(buf) - buf_sz] = '\n';

	//printf("Debug: sizeof: %d\nContents: { ", sizeof(buf) - buf_sz);

	do{
		buf[sizeof(buf) - buf_sz - 1] = x % 10 + '0'; // Push first digit into buffer as char
		//buf[buf_sz++] = x % 10 + '0'; // Push last digit into buffer
		buf_sz++;
		x /= 10; // Remove last digit
	} while(x);

	//printf("%s }\n", &buf[sizeof(buf) - buf_sz]);
	//write(1, buf, buf_sz); // Using the write syscall to generate clean assembly

	// Rewritten to work with backwards
	write(1, &buf[sizeof(buf) - buf_sz], buf_sz);
}

int main(void) {
	
	dump(69420);
	dump(0);
	return 0;
}
