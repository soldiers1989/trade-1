#include "mm.h"

BEGIN_CUBE_NAMESPACE
int mm::max_same_prefix_and_postfix(const char* blk, int len) {
	int rptlen = 0;
	for (rptlen = len - 1; rptlen > 0; rptlen--) {
		bool same = true;
		for (int i = 0, j = len - rptlen; i < rptlen; i++, j++) {
			if (*(blk + i) != *(blk + j)) {
				same = false;
				break;
			}
		}

		if (same) {
			return rptlen;
		}
	}
	return 0;
}

char* mm::fast_search(char* content, int content_length, const char* target, int target_length) {
	int * next = new int[target_length];
	for (int sublen = 0; sublen < target_length; sublen++) {
		next[sublen] = mm::max_same_prefix_and_postfix(target, sublen + 1) + 1;
	}

	int i = 0, j = 0;
	while (i < content_length - target_length + 1 && j < target_length) {
		for (j = 0; j < target_length; j++) {
			if (*(content + i + j) != *(target + j)) {
				i += next[j];
				break;
			}
		}
	}

	if (i < content_length - target_length) {
		return (char*)content + i;
	}

	return 0;
}

char* mm::slow_search(char* content, int content_length, const char* target, int target_length) {
	int i = 0, j = 0;
	for (i = 0; i < content_length - target_length + 1; i++) {
		for (j = 0; j < target_length; j++) {
			if (*(content + i + j) != *(target + j)) {
				break;
			}
		}
		if (j == target_length) {
			break;
		}
	}
	if (i < content_length - target_length + 1) {
		return (char*)(content + i);
	}

	return 0;
}

char* mm::search(char* content, int content_length, const char* target, int target_length, bool fast/* = true*/) {
	if (fast) {
		return mm::fast_search(content, content_length, target, target_length);
	} else {
		return mm::slow_search(content, content_length, target, target_length);
	}
}

int mm::overwrite(char* data, int datalen, const char* src, int srclen, const char* dest, int destlen, char default/* = 0*/, bool onlyfirst/* = true*/) {
	//overwrite number
	int ownum = 0;

	while (data != 0 && datalen > 0) {
		//first search the source position in data
		char* pdata = mm::search(data, datalen, src, srclen);
		if (destlen > srclen && (datalen - (pdata - data) < destlen))
			break;

		//overwrite with destination data
		if (destlen < srclen)
			memset(pdata, default, srclen);
		memcpy(pdata, dest, destlen);
		ownum++;

		if (onlyfirst)
			break;

		//next search from new position
		data = pdata + (destlen > srclen ? destlen : srclen);
		datalen = datalen - (destlen > srclen ? destlen : srclen);
	}

	return ownum;
}


END_CUBE_NAMESPACE
