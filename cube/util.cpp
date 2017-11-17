#include "cube/util.h"

namespace cube {
	/*
	*	get the max length of the same prefix and postfix of input data sequence block.
	*for example:
	*	input data block: <abadaba>,  prefix: <a,ab, aba, abad, abada, abadab>, postfix:<a, ba, aba, daba, adaba, badaba>
	*same prefix and postfix is<a, aba>, and the max is <aba>, its length is 3 which will be returned.
	*@param blk: data sequence block
	*@param len: length of input data block in bytes
	*@return:
	*	max length of the same prefix and postfix
	*/
	int max_same_prefix_and_postfix(const cube::byte* blk, int len) {
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

	/*
	*	search a target data block in the content data block, return the position of the first
	*ocurrence in the content
	*@param content: content data block to search
	*@param content_length: size of the content data block in bytes
	*@param target: target target data to search
	*@param target_length: size of the target data block in bytes
	*@return
	*	pointer to the first occurence of @target in the @content block, or 0 if target not found.
	*/
	cube::byte* fast_search(const cube::byte* content, int content_length, const cube::byte* target, int target_length) {
		int * next = new int[target_length];
		for (int sublen = 0; sublen < target_length; sublen++) {
			next[sublen] = max_same_prefix_and_postfix(target, sublen + 1) + 1;
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
			return (cube::byte*)content + i;
		}

		return 0;
	}

	cube::byte* slow_search(const cube::byte* content, int content_length, const cube::byte* target, int target_length) {
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
			return (cube::byte*)(content + i);
		}

		return 0;
	}
}
