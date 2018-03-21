#include "cube\str\rand.h"
BEGIN_CUBE_STR_NS
std::string str::random(int len) {
	//string set for peeking the random character
	const static std::string strset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

	//generate random string
	std::string randstr("");
	for (int i = 0; i < len; i++) {
		int pos = rand() % strset.length();
		randstr.append(1, strset[pos]);
	}

	return randstr;
}
END_CUBE_STR_NS
