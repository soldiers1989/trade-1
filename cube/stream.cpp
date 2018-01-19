#include "stream.h"
BEGIN_CUBE_NAMESPACE
//////////////////////////////////////////piped stream class//////////////////////////////////////
int pipedstream::put(const char *data, int sz) {
	if (_stream != 0) {
		return _stream->put(data, sz);
	}
	return _put(data, sz);
}

int pipedstream::get(char *data, int sz) {
	if (_stream != 0) {
		return _stream->get(data, sz);
	}
	return _get(data, sz);
}

bool pipedstream::endp() {
	if (_stream != 0) {
		return _stream->endp();
	}
	return _endp();
}

bool pipedstream::endg() {
	if (_stream != 0) {
		return _stream->endg();
	}
	return _endg();
}

int pipedstream::size() {
	if (_stream != 0) {
		return _stream->size();
	}
	return _size();
}

const char *pipedstream::data() {
	if (_stream != 0) {
		return _stream->data();
	}
	return _data();
}

//////////////////////////////////////////string stream class//////////////////////////////////////
int sstream::read(char *data, int sz) {
	if (_rpos < _wpos) {
		//get read size
		int rsz = _wpos - _rpos > sz ? sz : _wpos - _rpos;
		//copy to destination data buffer
		memcpy(data, _data.c_str(), rsz);
		//reset current read pos
		_rpos += rsz;
		//return read size
		return rsz;
	}

	//read nothing
	return 0;
}

//////////////////////////////////////////sized stream class//////////////////////////////////////
int sizedstream::write(const char *data, int sz) {
	//stream has completed
	if (full()) {
		return 0;
	}

	//get want size
	int want = _size - _data.length();
	want = sz > want ? want : sz;

	//need more data
	if (want > 0) {
		//append more data
		_data.append(data, want);
		_wpos = _data.length();

		//set flag if completed
		if (_wpos == _size) {
			full(true);
		}
	}

	return want;
}

//////////////////////////////////////////delimited stream class////////////////////////////////////////
int delimitedstream::write(const char *data, int sz) {
	//streamer is full
	if (full()) {
		return 0;
	}

	//restore last delimiter match result
	int szdelimiter = _delimiter.length();
	const char *delimiter = _delimiter.c_str(), *pdelimiter = delimiter + _currpos;

	//continue check the end tag
	const char *pdata = data, *sdata = data;
	while (pdata - data < sz && pdelimiter - delimiter < szdelimiter) {
		if (*pdelimiter != *pdata) {
			//move data pos to next position
			sdata = ++pdata;
			//reset delimiter pos
			pdelimiter = delimiter;
		} else {
			pdata++;
			pdelimiter++;
		}
	}

	//delimiter found in stream
	if (pdelimiter - delimiter == szdelimiter) {
		//set completed flag
		full(true);
		//write data
		int wsz = pdata - data;
		_data.append(data, wsz);
		//return write size
		return wsz;
	}

	//delimiter not found, save current matched pos
	_currpos = pdelimiter - delimiter;

	//write all data
	_data.append(data, sz);

	//all data feeded
	return sz;
}
END_CUBE_NAMESPACE
