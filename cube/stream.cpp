#include "stream.h"
BEGIN_CUBE_NAMESPACE
//////////////////////////////////////////sized stream stream class//////////////////////////////////////
int sizedstream::read(char *data, int sz) {
	return 0;
}

int sizedstream::write(const char *data, int sz) {
	//check if stream has completed
	if (completed()) {
		return 0;
	}

	//get want size
	int want = _size - _str.length();
	want = sz > want ? want : sz;

	//stream has completed
	if (want > 0) {
		_str.append(data, want);

		//set flag if completed
		if (_str.length() == _size) {
			complete(true);
		}
	}

	return want;
}

//////////////////////////////////////////streamer class////////////////////////////////////////
int delimitedstream::read(char *data, int sz) {
	return 0;
}

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
		_str.append(data, wsz);
		//return write size
		return wsz;
	}

	//delimiter not found, save current matched pos
	_currpos = pdelimiter - delimiter;

	//write all data
	_str.append(data, sz);

	//all data feeded
	return sz;
}
END_CUBE_NAMESPACE
