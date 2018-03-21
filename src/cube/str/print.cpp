#include "cube\str\print.h"
#include <iomanip>
#include <iostream>
BEGIN_CUBE_STR_NS
void print(const std::vector<std::vector<std::string>> &table, int colwidth) {
	for (size_t nrow = 0; nrow < table.size(); nrow++) {
		for (size_t ncol = 0; ncol < table[nrow].size(); ncol++) {
			std::cout << std::setw(colwidth) << table[nrow][ncol].c_str();
		}
		std::cout << std::endl;
	}
}
END_CUBE_STR_NS
