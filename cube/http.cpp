#include "http.h"
BEGIN_CUBE_NAMESPACE
BEGIN_HTTP_NAMESPACE

uri::uri() {

}

uri::~uri() {

}

int uri::parse(const std::string &str, std::string *error) {
	return 0;
}

int uri::parse(const char *str, int sz, std::string *error) {
	return 0;
}

int uri::pack(std::string &str, std::string *error) {
	return 0;
}

END_HTTP_NAMESPACE
END_CUBE_NAMESPACE
