#include "servlet.h"

int login::handle(const cube::http::request &req, cube::http::response &resp) {
	std::string content("hello");
	resp.set_content(content.c_str(), content.length(), "text/json");
	return 0;
}
