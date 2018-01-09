#include <io.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <direct.h>
#include <sys/stat.h>

#include "fd.h"
#include "str.h"

BEGIN_CUBE_NAMESPACE
////////////////////////////////////////////////file/directory class//////////////////////////////////////////////////
const char* fd::SEP = "\\";

bool fd::exist(const std::string &path) {
	if (_access(path.c_str(), 0) == 0) {
		return true;
	}
	return false;
}

bool fd::isdir(const std::string &path) {
	struct _stat stat;
	if (_stat(path.c_str(), &stat) == 0 && (stat.st_mode&S_IFDIR) == S_IFDIR) {
		return true;
	}

	return false;
}

bool fd::isfile(const std::string &path) {
	struct _stat stat;
	if (_stat(path.c_str(), &stat) == 0 && (stat.st_mode&S_IFREG) == S_IFREG) {
		return true;
	}

	return false;
}

int fd::stat(int fd, filestat &fstat) {
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

int fd::stat(const std::string &path, filestat &fstat) {
	int fd = ::_open(path.c_str(), 0);
	if (fd < 0)
		return -1;

	int err = stat(fd, fstat);
	::_close(fd);

	return err;
}

int fd::size(int fd, size_t &sz) {
	long len = _filelength(fd);
	if (len == -1)
		return -1;
	sz = len;
	return 0;
}

int fd::size(const std::string &path, size_t &sz) {
	int fd = ::_open(path.c_str(), 0);
	if (fd < 0)
		return -1;

	int err = size(fd, sz);
	::_close(fd);

	return err;
}

std::string fd::name(const std::string &path) {
	std::vector<std::string> subpaths = str::splits(path.c_str(), "\\/");
	if (subpaths.size() > 0) {
		return subpaths[subpaths.size() - 1];
	}

	return "";
}

std::string fd::path(const std::string &path) {
	std::vector<std::string> subpaths = str::splits(path.c_str(), "\\/");
	if (subpaths.size() > 0) {
		std::string filename = subpaths[subpaths.size() - 1];
		return path.substr(0, path.length() - filename.length());
	}
	return "";
}

std::vector<findres> fd::find(const std::string &path, const char* spec/* = "*"*/, int attrib/* = attrib::ALL*/, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	std::vector<findres> results;
	struct _finddata_t fdata;
	intptr_t hd = 0;

	std::string paths = path::make(path, spec);
	if ((hd = _findfirst(paths.c_str(), &fdata)) != -1) {
		do {
			if ((attrib == attrib::ALL || (fdata.attrib & (unsigned)attrib) != 0) && (onlyvisible && *fdata.name != '.')) {
				if (onlyname) {
					results.push_back(findres(fdata.name, fdata.size, fdata.time_create, fdata.time_access, fdata.time_write, fdata.attrib));
				} else {
					results.push_back(findres(path::make(path, fdata.name).c_str(), fdata.size, fdata.time_create, fdata.time_access, fdata.time_write, fdata.attrib));
				}
			}
		} while (_findnext(hd, &fdata) == 0);
		_findclose(hd);
	}

	return results;
}

std::vector<std::string> fd::finds(const std::string &path, const char* spec/* = "*"*/, int attrib/* = attrib::ALL*/, bool onlyvisible/* = true*/,  bool onlyname/* = true*/) {
	std::vector<std::string> results;
	struct _finddata_t fdata;
	intptr_t hd = 0;

	std::string paths = path::make(path, spec);
	if ((hd = _findfirst(paths.c_str(), &fdata)) != -1) {
		do {
			if ((attrib == attrib::ALL || (fdata.attrib & (unsigned)attrib) != 0) && (onlyvisible && *fdata.name != '.')) {
				if (onlyname) {
					results.push_back(fdata.name);
				}
				else {
					results.push_back(path::make(path, fdata.name));
				}
			}
		} while (_findnext(hd, &fdata) == 0);
		_findclose(hd);
	}
		return results;
}

std::vector<std::string> fd::dirs(const std::string &path, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	return finds(path, "*", attrib::DIR, onlyvisible, onlyname);
}

std::vector<std::string> fd::files(const std::string &path, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	return finds(path, "*", attrib::FILE, onlyvisible, onlyname);
}

////////////////////////////////////////////////path class//////////////////////////////////////////////////
std::string path::make(const std::string &parent, const std::string &child) {
	//trim parent's and child's left path seperators, add seperator between them
	return str::rstrip(str::rstrip(parent), fd::SEP) + fd::SEP + str::lstrip(str::rstrip(child), fd::SEP);
}

////////////////////////////////////////////////file class//////////////////////////////////////////////////
int file::read(const std::string &path, std::string &data) {
	//clear out data first
	data.clear();

	//read content from file
	std::ifstream ifs(path, std::ifstream::in | std::ifstream::binary);
	if (!ifs.is_open())
		return -1;

	//read buffer
	const std::streamsize BUFSZ = 32*1024;
	char buf[BUFSZ] = { 0 };

	//process each file line
	ifs.read(buf, BUFSZ);
	while (ifs.gcount() > 0) {
		//append data
		data.append(buf, (size_t)ifs.gcount());
		
		//check file
		if (!ifs.good())
			break;

		//next line
		ifs.read(buf, BUFSZ);
	}

	return 0;
}


char* file::read(const std::string &path, int &sz) {
	// open file
	FILE * pf = fopen(path.c_str(), "rb");
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

int file::write(const std::string &path, const char* content, int sz) {
	//open file
	FILE * pf = fopen(path.c_str(), "wb");
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

////////////////////////////////////////////////directory class//////////////////////////////////////////////////
int dir::mkdir(const std::string &path) {
	int err = _mkdir(path.c_str());
	if (err != 0 && errno != EEXIST) {
		return -1;
	}
	return 0;
}

int dir::mkdirs(const std::string &path) {
	//check path parameter
	if (path == "") {
		return 0;
	}

	//directory already exist
	if (fd::exist(path) && fd::isdir(path)) {
		return 0;
	}

	//get parent directory
	size_t pos1 = path.find_last_of('/'), pos2 = path.find_last_of('\\'), lastpos = std::string::npos;
	if (pos1 != std::string::npos && pos2 != std::string::npos) {
		size_t lpos = pos1 < pos2 ? pos1 : pos2, rpos = pos1 < pos2 ? pos2 : pos1, pos = lpos + 1;
		while (pos < rpos) {
			if (path[pos] != '\\' && path[pos] != '/')
				break;
			pos++;
		}
		lastpos = pos < rpos ? rpos : lpos;
	} else if (pos1 != std::string::npos)
		lastpos = pos1;
	else if (pos2 != std::string::npos)
		lastpos = pos2;
	else
		lastpos = std::string::npos;

	if (lastpos != std::string::npos) {
		// create parent directory
		std::string parent_path = path.substr(0, lastpos);
		int err = mkdirs(parent_path);
		if (err != 0)
			return -1;
	}

	//create current directory
	return mkdir(path);
}
END_CUBE_NAMESPACE
