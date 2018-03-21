#include "cube\str\strip.h"
#include "cube\http\stream.h"
BEGIN_CUBE_HTTP_NS
//////////////////////////////data stream class/////////////////////////////////
int data_stream::open() {
	return 0; //do nothing
}

size_t data_stream::read(char *data, size_t sz) {
	//current data size
	size_t csz = _data.length();

	//no more data for reading
	if (!(_rpos < csz))
		return 0;

	//get read size
	size_t rsz = csz - _rpos > sz ? sz : csz - _rpos;
	//copy to destination data buffer
	memcpy(data, _data.c_str()+_rpos, (::size_t)rsz);
	//reset current read pos
	_rpos += rsz;
	//return read size
	return rsz;
}

size_t data_stream::write(const char *data, size_t sz) {
	//current stream size
	size_t csz = _data.length();

	//no more space for writting
	if (!(_wpos < csz))
		return 0;

	//left space for writting
	size_t left = _msz - _wpos;
	//get write size
	size_t wsz = sz > left ? left : sz;

	if (_wpos == csz) {
		//append data
		_data.append(data, (::size_t)wsz);
	} else {
		//replace data
		_data.replace((::size_t)_wpos, (::size_t)wsz, data, (::size_t)wsz);
	}

	//reset the write position
	_wpos += wsz;

	return wsz;
}

size_t data_stream::seekr(size_t pos) {
	//current stream data size
	size_t csz = _data.length();
	//seek read position to stream end when specified position if more thran data size
	if (!(pos < _data.length())) {
		pos = csz;
	}
	//set current read position
	_rpos = pos;
	return _rpos;
}

size_t data_stream::seekw(size_t pos) {
	//current stream data size
	size_t csz = _data.length();

	//set too large pos to max data size
	if (pos > _msz) {
		pos = _msz;
	}

	//add blank character
	if (pos > csz) {
		//add blank data
		size_t blanksz = pos - csz;
		_data.append((::size_t)blanksz, 0);
	}

	//set write position
	_wpos = pos;

	return _wpos;
}

size_t data_stream::tellr() const {
	return _rpos;
}

size_t data_stream::tellw() const {
	return _wpos;
}

bool data_stream::endr() const {
	return !(_rpos < _data.length());
}

bool data_stream::endw() const {
	return _wpos == _data.length();
}

bool data_stream::full() const {
	return !(_data.length() < _msz);
}

bool data_stream::empty() const {
	return _data.length() == 0;
}

size_t data_stream::size() const {
	return _data.length();
}

std::string data_stream::data() {
	return _data;
}

void data_stream::flush() {
	;//do nothing
}

void data_stream::close() {
	;//do nothing
}


//////////////////////////////////////////file stream class//////////////////////////////////////
int file_stream::open() {
	//file must be opened after construct
	if (!_file.is_open()) {
		return -1;
	}
	
	//get current file size
	_csz = _size();
	
	//set current write position
	_wpos = _csz;

	return 0;
}

size_t file_stream::read(char *data, size_t sz) {
	//no more data for reading
	if (!(_rpos < _csz))
		return 0;

	//read data
	_file.read(data, sz);
	//get read size
	size_t rsz = (size_t)_file.gcount();
	//set read position
	_rpos += rsz;

	return rsz;
}

size_t file_stream::write(const char *data, size_t sz) {
	//no more space for writting
	if (!(_wpos < _msz))
		return 0;

	//left space for writting
	size_t left = _msz - _wpos;
	//get write size
	size_t wsz = sz > left ? left : sz;

	//write data
	_file.write(data, wsz);
	//set write position
	_wpos += wsz;

	//set current file size
	if (_wpos > _csz)
		_csz = _wpos;

	return wsz;
}

size_t file_stream::seekr(size_t pos) {
	//seek to file end if pos > current file size
	if (!(pos < _csz)) {
		pos = _csz;
	}
		
	//seek to specified read position
	_file.seekg(pos);

	//reset the read position
	_rpos = pos;

	return _rpos;
}

size_t file_stream::seekw(size_t pos) {
	//set too large pos to max data size
	if (pos > _msz) {
		pos = _msz;
	}

	//add blank character
	if (pos > _csz) {
		//seek write pos to file end
		if (_wpos != _csz) {
			_file.seekp(_csz);
		}

		//blank block data
		const int BLOCKSZ = 16 * 1024;
		char blockdata[BLOCKSZ] = { 0 };

		//blank data size need to add
		size_t blanksz = pos - _csz;
		size_t blocks = blanksz / BLOCKSZ;
		//write blank data to file
		for (size_t i = 0; i < blocks; i++) {
			_file.write(blockdata, BLOCKSZ);
		}

		//write left blank data
		size_t leftsz = blanksz % BLOCKSZ;
		if (leftsz > 0) {
			_file.write(blockdata, leftsz);
		}
	} else {
		//seek to specified posotion
		_file.seekp(pos);
	}

	//set write position
	_wpos = pos;
	
	return _wpos;
}

size_t file_stream::tellr() const {
	return _rpos;
}

size_t file_stream::tellw() const {
	return _wpos;
}

bool file_stream::endw() const {
	return _wpos == _csz;
}

bool file_stream::endr() const {
	return _rpos == _csz;
}

bool file_stream::full() const {
	return _wpos == _msz;
}

bool file_stream::empty() const {
	return _csz == 0;
}

size_t file_stream::size() const {
	return _csz;
}

void file_stream::flush() {
	_file.flush();
}

void file_stream::close() {
	_file.close();
}

std::string file_stream::data() {
	std::string data("");

	//save current get position
	std::streampos gpos = _file.tellg();

	//set get pos to start
	_file.seekg(0);

	//read file content
	const int BUFSZ = 16 * 1024;
	char buf[BUFSZ] = { 0 };
	while (!_file.eof()) {
		_file.read(buf, BUFSZ);
		data.append(buf, (::size_t)_file.gcount());
	}

	//reset get position
	_file.seekg(gpos, std::ios::beg);

	//return content read
	return data;
}

size_t file_stream::_size() {
	//save current get position
	std::streampos gpos = _file.tellg();

	//get file size
	_file.seekg(0, std::ios::end);
	size_t sz = (size_t)_file.tellg();

	//restore get position
	_file.seekg(gpos, std::ios::beg);

	return sz;
}
END_CUBE_HTTP_NS
