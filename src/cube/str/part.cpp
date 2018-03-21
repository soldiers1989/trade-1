#include "cube\str\part.h"
BEGIN_CUBE_STR_NS

std::vector<std::string> part(const char *str, const char *delimiters, int maxwant) {
	std::vector<std::string> result;
	part(str, delimiters, result, maxwant);
	return result;
}

void part(const char *str, const char *delimiters, std::vector<std::string> &result, int maxwant) {
	//clear result
	result.clear();

	//split string
	const char *start = str;
	while ((int)result.size() < maxwant - 1) {
		//find first split start pos
		while (*start != 0 && ::strchr(delimiters, *start) != 0)
			start++;

		//find first split end pos
		if (*start != 0) {
			const char *end = start + 1;
			while (*end != 0 && ::strchr(delimiters, *end) == 0)
				end++;

			result.push_back(std::string(start, end - start));

			//continue next split
			if (*end != 0)
				start = end + 1;
			else {
				start = end;
				break;
			}
		} else {
			break;
		}
	}

	//push the end string
	while (*start != 0 && ::strchr(delimiters, *start) != 0)
		start++;
	if (*start != 0) {
		result.push_back(start);
	}
}

std::vector<std::string> part(const char *str, int sz, const char *delimiters, int maxwant) {
	std::vector<std::string> result;
	part(str, sz, delimiters, result, maxwant);
	return result;
}

void part(const char *str, int sz, const char *delimiters, std::vector<std::string> &result, int maxwant) {
	//clear result
	result.clear();

	//split string
	const char *start = str;
	while ((int)result.size() < maxwant - 1) {
		//find first split start pos
		while (start - str < sz && ::strchr(delimiters, *start) != 0)
			start++;

		//find first split end pos
		if (start - str < sz) {
			const char *end = start + 1;
			while (end - str < sz && ::strchr(delimiters, *end) == 0)
				end++;
			result.push_back(std::string(start, end - start));

			//continue next split
			if (end - str < sz)
				start = end + 1;
			else {
				start = end;
				break;
			}
		} else {
			break;
		}
	}

	//push the end string
	while (start - str < sz && ::strchr(delimiters, *start) != 0)
		start++;
	if (start - str < sz) {
		result.push_back(std::string(start, sz - (start - str)));
	}
}
END_CUBE_STR_NS
