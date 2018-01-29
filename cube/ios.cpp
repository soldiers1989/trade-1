#include "ios.h"
BEGIN_IOS_NAMESPACE
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

bool stream::endp() const {
	if (_stream != 0) {
		return _stream->endp();
	}
	return _endp();
}

bool stream::endg() const {
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

const std::string &stream::data() {
	if (_stream != 0) {
		return _stream->data();
	}
	return _data();
}

void stream::assign(const std::string &data) {
	if (_stream != 0) {
		_stream->assign(data);
	} else {
		_assign(data);
	}
}

//////////////////////////////////////////string stream class//////////////////////////////////////
int stringstream::_put(const char *data, int sz) {
	if (!endp()) {
		_stream.append(data, sz);
		return sz;
	}

	return 0;
}

int stringstream::_get(char *data, int sz) {
	//still has left data
	if (!endg()) {
		int len = (int)_stream.length();
		//get read size
		int rsz = len - _rpos > sz ? sz : len - _rpos;
		//copy to destination data buffer
		memcpy(data, _stream.c_str(), rsz);
		//reset current read pos
		_rpos += rsz;
		//return read size
		return rsz;
	}

	//no more data left
	return 0;
}

//////////////////////////////////////////sized stream class//////////////////////////////////////
int sizedstream::_put(const char *data, int sz) {
	//stream not completed, put more data
	if (!endp()) {
		int len = (int)_stream.length();
		int wsz = len + sz < _dsize ? sz : sz - len;
		_stream.append(data, wsz);
		return wsz;
	}

	//stream has completed
	return 0;
}

int sizedstream::_get(char *data, int sz) {
	if (!endg()) {
		int len = (int)_stream.length();
		//get read size
		int rsz = len - _rpos > sz ? sz : len - _rpos;
		//copy to destination data buffer
		memcpy(data, _stream.c_str(), rsz);
		//reset current read pos
		_rpos += rsz;
		//return read size
		return rsz;
	}

	//no more data
	return 0;
}

//////////////////////////////////////////delimiter stream class//////////////////////////////////////
int delimitedstream::_put(const char *data, int sz) {
	//stream not completed, need more data
	if (!endp()) {
		//restore last delimiter match result
		int szdelimiter = _delimiter.length();
		const char *delimiter = _delimiter.c_str(), *pdelimiter = delimiter + _dpos;

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
			_full = true;
			//write data
			int wsz = pdata - data;
			_stream.append(data, wsz);
			//return write size
			return wsz;
		}

		//delimiter not found, save current matched pos
		_dpos = pdelimiter - delimiter;

		//write all data
		_stream.append(data, sz);

		//all data feeded
		return sz;
	}

	//stream has completed
	return 0;
}

int delimitedstream::_get(char *data, int sz) {
	if (!endg()) {
		int len = (int)_stream.length();
		//get read size
		int rsz = len - _rpos > sz ? sz : len - _rpos;
		//copy to destination data buffer
		memcpy(data, _stream.c_str(), rsz);
		//reset current read pos
		_rpos += rsz;
		//return read size
		return rsz;
	}

	//no more data
	return 0;
}

//////////////////////////////////////////file stream class//////////////////////////////////////
int filestream::_put(const char *data, int sz) {
	_file.write(data, sz);
	return sz;
}

int filestream::_get(char *data, int sz) {
	_file.read(data, sz);
	return (int)_file.gcount();
}

bool filestream::_endp() const {
	return false;
}

bool filestream::_endg() const {
	return _file.eof();
}

int filestream::_size() {
	//save current get pos
	std::streampos gpos = _file.tellg();

	//get file size
	_file.seekg(0, std::ios::end);
	std::streampos sz = _file.tellg();

	//restore get pos
	_file.seekg(gpos, std::ios::beg);

	return (int)sz;
}

void filestream::_assign(const std::string &data) {
	_file.write(data.c_str(), data.length());
	_file.flush();
}

const std::string &filestream::_data() {
	//content has read before
	if (!_content.empty())
		return _content;

	//save current get pos
	std::streampos gpos = _file.tellg();

	//set get pos to start
	_file.seekg(0);

	//read file content
	char buf[BUFSZ] = { 0 };
	while (!_file.eof()) {
		_file.read(buf, BUFSZ);
		_content.append(buf, (size_t)_file.gcount());
	}

	//return content read
	return _content;
}
END_IOS_NAMESPACE
