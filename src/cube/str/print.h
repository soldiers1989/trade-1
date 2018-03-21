#pragma once
#include <vector>
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	print table data to console
*@param table: in, table want to print
*@return
*	void
*/
void print(const std::vector<std::vector<std::string>> &table, int colwidth = 10);
END_CUBE_STR_NS
