#include <stdio.h>

#define SV_IMPLEMENTATION
#include "./sv.h"

int main() {

	String_View source = SV("    34       35 +   .    asdajs");
	const char *start = source.data; // Contains the starting position

	source = sv_trim_left(source); // Trim before if the line is only spaces
	while(source.count > 0) {
		String_View token = sv_chop_by_delim(&source, ' ');
		size_t col = token.data - start; // Contains the current position
		printf("Token: "SV_Fmt" (%zu)\n", SV_Arg(token), col);
		source = sv_trim_left(source); // Keep trimming
	}

	return 0;
}
