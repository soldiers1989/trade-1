#include "cube\table.h"
#include "cube\str.h"

BEGIN_CUBE_NAMESPACE
std::vector<std::vector<std::string>> table::load(const char *data, const char *seprow, const char *sepcol) {
	std::vector<std::vector<std::string>> table;

	std::vector<std::string> rows = cube::str::split(data, seprow);
	for (int i = 0; i < (int)rows.size(); i++) {
		std::vector<std::string> cols = cube::str::split(rows[i], sepcol);
		table.push_back(cols);
	}

	return table;
}
END_CUBE_NAMESPACE
