#include <string.h>
#include "cube\str\find.h"

BEGIN_CUBE_STR_NS
char * find(char *str, int sz, int ch) {
	return (char*)::memchr(str, ch, sz);
}

const char * find(const char *str, int sz, int ch) {
	return (const char*)::memchr(str, ch, sz);
}

char *find(char *str, int sz, const char *substr) {
	char *pos = str;
	while (pos - str < sz) {
		char *ppos = pos;
		const char *spos = substr;
		while (*spos != 0 && ppos - str < sz && *ppos == *spos) {
			spos++;
			ppos++;
		}

		if (*spos == 0)
			return pos;
		else
			pos++;
	}

	return 0;
}

const char *find(const char *str, int sz, const char *substr) {
	const char *pos = str;
	while (pos - str < sz) {
		const char *spos = substr, *ppos = pos;
		while (*spos != 0 && ppos - str < sz && *ppos == *spos) {
			spos++;
			ppos++;
		}

		if (*spos == 0)
			return pos;
		else
			pos++;
	}

	return 0;
}
END_CUBE_STR_NS
