#include <io.h>
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

std::string fd::name(const std::string &path) {
	std::vector<std::string> subpaths = str::splits(path, "\\/");
	if (subpaths.size() > 0) {
		return subpaths[subpaths.size() - 1];
	}

	return "";
}

std::string fd::path(const std::string &path) {
	std::vector<std::string> subpaths = str::splits(path, "\\/");
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

	std::string paths = path + SEP + spec;
	if ((hd = _findfirst(paths.c_str(), &fdata)) != -1) {
		do {
			if ((attrib == attrib::ALL || (fdata.attrib & (unsigned)attrib) != 0) && (onlyvisible && *fdata.name != '.')) {
				if (onlyname) {
					results.push_back(findres(fdata.name, fdata.size, fdata.time_create, fdata.time_access, fdata.time_write, fdata.attrib));
				} else {
					std::string fullpath = path + SEP + std::string(fdata.name);
					results.push_back(findres(fullpath.c_str(), fdata.size, fdata.time_create, fdata.time_access, fdata.time_write, fdata.attrib));
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

	std::string paths = path + SEP + spec;
	if ((hd = _findfirst(paths.c_str(), &fdata)) != -1) {
		do {
			if ((attrib == attrib::ALL || (fdata.attrib & (unsigned)attrib) != 0) && (onlyvisible && *fdata.name != '.')) {
				if (onlyname) {
					results.push_back(fdata.name);
				}
				else {
					std::string fullpath = path + SEP + std::string(fdata.name);
					results.push_back(fullpath);
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

////////////////////////////////////////////////file class//////////////////////////////////////////////////
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
