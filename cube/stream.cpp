#include "stream.h"
BEGIN_CUBE_NAMESPACE
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
	if (completed()) {
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
			complete(true);
		}
	}

	return want;
}

//////////////////////////////////////////delimited stream class////////////////////////////////////////
int delimitedstream::write(const char *data, int sz) {
	//streamer is full
	if (completed()) {
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
		complete(true);
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