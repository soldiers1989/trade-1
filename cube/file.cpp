#include <io.h>
#include <stdio.h>
#include <stdlib.h>
#include <direct.h>
#include <sys/stat.h>
#include "file.h"
#include "util.h"

BEGIN_CUBE_NAMESPACE
file::file()
{
}

file::~file()
{
}

bool file::exist(std::string path) {
	if (_access(path.c_str(), 0) == 0) {
		return true;
	}
	return false;
}

bool file::isfile(std::string path) {
	struct _stat stat;
	if (_stat(path.c_str(), &stat) == 0 && (stat.st_mode&S_IFREG) == S_IFREG) {
		return true;
	}

	return false;
}


bool file::isdir(std::string path) {
	struct _stat stat;
	if (_stat(path.c_str(), &stat) == 0 && (stat.st_mode&S_IFDIR) == S_IFDIR) {
		return true;
	}

	return false;
}

std::string file::filename(std::string path) {
	std::vector<std::string> subpaths = util::splits(path, "\\/");
	if (subpaths.size() > 0) {
		return subpaths[subpaths.size() - 1];
	}

	return "";
}

std::string dirpath(std::string path) {
	std::vector<std::string> subpaths = util::splits(path, "\\/");
	if (subpaths.size() > 0) {
		std::string filename = subpaths[subpaths.size() - 1];
		return path.substr(0, path.length() - filename.length());
	}
	return "";
}

int file::mkdir(std::string path) {
	int err = _mkdir(path.c_str());
	if (err != 0 && errno != EEXIST) {
		return -1;
	}
	return 0;
}

int file::mkdirs(std::string path) {
	//check path parameter
	if (path == "") {
		return 0;
	}

	//directory already exist
	if (file::exist(path) && file::isdir(path)) {
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
	}
	else if (pos1 != std::string::npos)
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
	return file::mkdir(path);
}

char* file::read(std::string path, int &sz) {
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
		delete []content;
		fclose(pf);
		return NULL;
	}

	//close file
	fclose(pf);

	//set data size read
	sz = file_size;

	return content;
	
}

int file::write(std::string path, const char* content, int sz) {
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
END_CUBE_NAMESPACE
