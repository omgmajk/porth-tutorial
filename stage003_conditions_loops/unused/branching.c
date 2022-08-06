#include <stdio.h>

int max(int a, int b) {
	return a < b ? b : a;
}

int main(void) {

	// Above function generates the following assembly with -O3
	/*
		cmp    edi, esi
		mov    eax, esi
		cmovge eax, edi
		ret
	*/

	return 0;
}
