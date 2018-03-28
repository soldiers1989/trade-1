#pragma once
#include <string>
#include <vector>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS

std::string json(const std::string &str);

/*
*	convert table to json array string
*@param table: in, table to convert
*@return:
*	json string
*/
std::string json(const std::vector<std::vector<std::string>> &table);
END_CUBE_STR_NS
