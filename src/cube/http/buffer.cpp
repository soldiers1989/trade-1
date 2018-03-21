#include <string.h>
#include "cube\http\buffer.h"
BEGIN_CUBE_HTTP_NS
int line_buffer::get(char *data, int sz) {
	int getsz = sz > (int)_data.length() ? (int)_data.length() : sz;
	memcpy(data, _data.c_str(), getsz);
	return getsz;
}

int line_buffer::put(const char *data, int sz) {
	int putsz = 0;
	while (_data.back() != '\n' && putsz < sz) {
		char c = *(data + putsz);
		_data.append(1, c);
		putsz++;
	}

	return putsz;
}

bool line_buffer::full() const {
	return _data.back() == '\n';
}

int line_buffer::size() const {
	return _data.length();
}

void line_buffer::clear() {
	_data.clear();
}

const char * line_buffer::data() const {
	return _data.c_str();
}

std::string line_buffer::line() const {
	//get data length
	size_t len = _data.length();

	//initialize start and end pos of data
	size_t spos = 0, epos = len - 1;
	//get buffer data pointer
	const char *data = _data.data();

	//skip start space characters
	while (spos < len && ::isspace(*(data + spos)))
		spos++;

	//skip end space characters
	while (epos > spos && ::isspace(*(data + epos)))
		epos--;

	return _data.substr(spos, epos - spos + 1);
}
END_CUBE_HTTP_NS
