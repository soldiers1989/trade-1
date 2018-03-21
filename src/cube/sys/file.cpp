#include <io.h>
#include <fstream>
#include <direct.h>
#include <sys/stat.h>
#include "cube\str\part.h"
#include "cube\sys\file.h"
BEGIN_CUBE_SYS_FILE_NS
bool exist(const std::string &path) {
	if (_access(path.c_str(), 0) == 0) {
		return true;
	}
	return false;
}

bool isdir(const std::string &path) {
	struct _stat stat;
	if (_stat(path.c_str(), &stat) == 0 && (stat.st_mode&S_IFDIR) == S_IFDIR) {
		return true;
	}

	return false;
}

bool isfile(const std::string &path) {
	struct _stat stat;
	if (_stat(path.c_str(), &stat) == 0 && (stat.st_mode&S_IFREG) == S_IFREG) {
		return true;
	}

	return false;
}

int stat(int fd, filestat &fstat) {
	//get file stat
	struct _stat st;
	int err = _fstat(fd, &st);
	if (err != 0)
		return -1;

	//set return stat
	fstat.mode = st.st_mode;
	fstat.size = st.st_size;
	fstat.atime = st.st_atime;
	fstat.ctime = st.st_ctime;
	fstat.mtime = st.st_mtime;

	return 0;
}

int stat(const std::string &path, filestat &fstat) {
	int fd = ::_open(path.c_str(), 0);
	if (fd < 0)
		return -1;

	int err = stat(fd, fstat);
	::_close(fd);

	return err;
}

int size(int fd, size_t &sz) {
	long len = _filelength(fd);
	if (len == -1)
		return -1;
	sz = len;
	return 0;
}

size_t size(const std::string &path) {
	size_t sz = 0;
	size(path, sz);
	return sz;
}

int size(const std::string &path, size_t &sz) {
	int fd = ::_open(path.c_str(), 0);
	if (fd < 0)
		return -1;

	int err = size(fd, sz);
	::_close(fd);

	return err;
}

std::string ext(const std::string &name) {
	std::size_t pos = name.rfind('.');
	if (pos != std::string::npos) {
		return name.substr(pos);
	}

	return "";
}

std::string name(const std::string &path) {
	std::vector<std::string> subpaths = str::part(path.c_str(), "\\/");
	if (subpaths.size() > 0) {
		return subpaths[subpaths.size() - 1];
	}

	return "";
}

std::string path(const std::string &path) {
	std::vector<std::string> subpaths = str::part(path.c_str(), "\\/");
	if (subpaths.size() > 0) {
		std::string filename = subpaths[subpaths.size() - 1];
		return path.substr(0, path.length() - filename.length());
	}
	return "";
}

int read(const std::string &path, std::string &data) {
	//clear out data first
	data.clear();

	//read content from file
	std::ifstream ifs(path, std::ifstream::in | std::ifstream::binary);
	if (!ifs.is_open())
		return -1;

	//read buffer
	const std::streamsize BUFSZ = 32 * 1024;
	char buf[BUFSZ] = { 0 };

	//process each file line
	ifs.read(buf, BUFSZ);
	while (ifs.gcount() > 0) {
		//append data
		data.append(buf, (std::size_t)ifs.gcount());

		//check file
		if (!ifs.good())
			break;

		//next line
		ifs.read(buf, BUFSZ);
	}

	return 0;
}


char* read(const std::string &path, int &sz) {
	// open file
	::FILE * pf = fopen(path.c_str(), "rb");
	if (pf == NULL) {
		return NULL;
	}

	// get file size
	int file_size = (int)_filelength(_fileno(pf));
	if (file_size < 0) {
		fclose(pf);
		return NULL;
	}

	//read data
	char *content = new char[file_size];
	size_t rdsz = fread(content, sizeof(char), file_size, pf);
	if (rdsz != (size_t)file_size) {
		delete[]content;
		fclose(pf);
		return NULL;
	}

	//close file
	fclose(pf);

	//set data size read
	sz = file_size;

	return content;

}

int write(const std::string &path, const char* content, int sz) {
	//open file
	::FILE * pf = fopen(path.c_str(), "wb");
	if (pf == NULL) {
		return -1;
	}

	//write to file
	size_t wsz = fwrite(content, sizeof(char), sz, pf);
	if (wsz != sz) {
		fclose(pf);
		return -1;
	}

	//close file
	fclose(pf);

	return 0;
}
END_CUBE_SYS_FILE_NS
