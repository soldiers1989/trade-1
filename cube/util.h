#pragma once
#include <vector>
#include <string>

#include "cube.h"

BEGIN_CUBE_NAMESPACE
class util
{
public:
	/*
	*	split a string by character seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const char* str, const char sep);

	/*
	*	split a string by string seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const char* str, const char* sep);

	/*
	*	split a string by character seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const std::string& str, const char sep);

	/*
	*	split a string by string seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const std::string& str, const std::string& sep);

	/*
	*	split a string to table structure by row and column seperator
	*@param str: string to be splited
	*@param seprow: row seperator
	*@param sepcol: column seperator
	*@return:
	*	split result
	*/
	static std::vector<std::vector<std::string>> split(const char *str, const char *seprow, const char *sepcol);

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
	static char* fast_search(const char* content, int content_length, const char* target, int target_length);

	/*
	*	slow search, search a target data block in the content data block, return the position of the first ocurrence in the content
	*@param content: content data block to search
	*@param content_length: size of the content data block in bytes
	*@param target: target target data to search
	*@param target_length: size of the target data block in bytes
	*@return
	*	pointer to the first occurence of @target in the @content block, or 0 if target not found.
	*/
	static char* slow_search(const char* content, int content_length, const char* target, int target_length);

	/*
	*	search wrapper, search a target data block in the content data block, return the position of the first ocurrence in the content
	*@param content: content data block to search
	*@param content_length: size of the content data block in bytes
	*@param target: target target data to search
	*@param target_length: size of the target data block in bytes
	*@return
	*	pointer to the first occurence of @target in the @content block, or 0 if target not found.
	*/
	static char* search(const char* content, int content_length, char* target, int target_length, bool fast = true);

	/*
	*	check if input string is empty
	*@param str: string to check
	*@return:
	*	true if input string is empty, otherwise false
	*/
	static bool empty(const char* str);

	/*
	*	convert numberic(int, long, float, double) to string
	*@param val: number input value
	*@param fmt: format of input value
	*@return:
	*	string of value
	*/
	template<class T> static std::string tostr(const T val, const char* fmt);
};
END_CUBE_NAMESPACE
