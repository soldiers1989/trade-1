/*
*	mm - memory operation module
*/
#pragma once
#include "cube.h"

BEGIN_CUBE_NAMESPACE
class mm {
public:
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
	static int max_same_prefix_and_postfix(const char* blk, int len);

	/*
	*	fast search, search a target data block in the content data block, return the position of the first ocurrence in the content
	*@param content: content data block to search
	*@param content_length: size of the content data block in bytes
	*@param target: target target data to search
	*@param target_length: size of the target data block in bytes
	*@return
	*	pointer to the first occurence of @target in the @content block, or 0 if target not found.
	*/
	static char* fast_search(char* content, int content_length, const char* target, int target_length);
	static const char* fast_search(const char* content, int content_length, const char* target, int target_length);

	/*
	*	slow search, search a target data block in the content data block, return the position of the first ocurrence in the content
	*@param content: content data block to search
	*@param content_length: size of the content data block in bytes
	*@param target: target target data to search
	*@param target_length: size of the target data block in bytes
	*@return
	*	pointer to the first occurence of @target in the @content block, or 0 if target not found.
	*/
	static char* slow_search(char* content, int content_length, const char* target, int target_length);
	static const char* slow_search(const char* content, int content_length, const char* target, int target_length);

	/*
	*	search wrapper, search a target data block in the content data block, return the position of the first ocurrence in the content
	*@param content: content data block to search
	*@param content_length: size of the content data block in bytes
	*@param target: target target data to search
	*@param target_length: size of the target data block in bytes
	*@return
	*	pointer to the first occurence of @target in the @content block, or 0 if target not found.
	*/
	static char* search(char* content, int content_length, const char* target, int target_length, bool fast = true);
	static const char* search(const char* content, int content_length, const char* target, int target_length, bool fast = true);

	/*
	*	overwrite source with destination in the given data, use default value if destinaiton length is less than source length
	*@param data: in/out, given data
	*@param datalen: in, sizeof data
	*@param src: in, source data to be overwrite
	*@param srclen: in, length of source data in bytes
	*@param dest: in, destiniation data
	*@param destlen: in, length of destinationdata in bytes
	*@param default: default value use to overwrite source if destination length is less than source
	*@return:
	*	place number overwrited, otherwise <0
	*/
	static int overwrite(char* data, int datalen, const char* src, int srclen, const char* dest, int destlen, char default = 0, bool onlyfirst = true);
};
END_CUBE_NAMESPACE
