#include "cube\str\json.h"
BEGIN_CUBE_STR_NS
std::string json(const std::vector<std::vector<std::string>> &table) {
	std::string res("[");
	
	for (std::size_t i = 0; i < table.size(); i++) {
		std::string item("[");
		for (std::size_t j = 0; j < table[i].size(); j++) {
			if(j>0)
				item.append(",\"");
			else
				item.append("\"");
			item.append(table[i][j]);
			item.append("\"");
		}
		item.append("]");

		if(i>0)
			res.append(",");

		res.append(item);
	}
	
	res.append("]");

	return res;
}
END_CUBE_STR_NS
