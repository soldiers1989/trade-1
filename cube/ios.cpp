#include "ios.h"
BEGIN_CUBE_NAMESPACE
//////////////////////////////////////////stream class//////////////////////////////////////
int stream::put(const char *data, int sz) {
	if (_stream != 0) {
		return _stream->put(data, sz);
	}
	return _put(data, sz);
}

int stream::get(char *data, int sz) {
	if (_stream != 0) {
		return _stream->get(data, sz);
	}
	return _get(data, sz);
}

bool stream::endp() {
	if (_stream != 0) {
		return _stream->endp();
	}
	return _endp();
}

bool stream::endg() {
	if (_stream != 0) {
		return _stream->endg();
	}
	return _endg();
}

int stream::size() {
	if (_stream != 0) {
		return _stream->size();
	}
	return _size();
}

const char *stream::data() {
	if (_stream != 0) {
		return _stream->data();
	}
	return _data();
}

//////////////////////////////////////////string stream class//////////////////////////////////////
int stringstream::_put(const char *data, int sz) {
	_data.append(data, sz);
	return sz;
}

int stringstream::_get(char *data, int sz) {
	//end of stream
	if (endg()) {
		return 0;
	}

	//

}
END_CUBE_NAMESPACE
