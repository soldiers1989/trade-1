#include <io.h>
#include <direct.h>
#include "cube\str\strip.h"
#include "cube\sys\path.h"
#include "cube\sys\file.h"

BEGIN_CUBE_SYS_PATH_NS
int mkdir(const std::string &path) {
	int err = _mkdir(path.c_str());
	if (err != 0 && errno != EEXIST) {
		return -1;
	}
	return 0;
}

int mkdirs(const std::string &path) {
	//check path parameter
	if (path == "") {
		return 0;
	}

	//directory already exist
	if (file::exist(path) && file::isdir(path)) {
		return 0;
	}

	//get parent directory
	std::size_t pos1 = path.find_last_of('/'), pos2 = path.find_last_of('\\'), lastpos = std::string::npos;
	if (pos1 != std::string::npos && pos2 != std::string::npos) {
		std::size_t lpos = pos1 < pos2 ? pos1 : pos2, rpos = pos1 < pos2 ? pos2 : pos1, pos = lpos + 1;
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

std::string mkpath(const std::string &parent, const std::string &child) {
	const char* SEP = "\\";

	//trim parent's and child's left path seperators, add seperator between them
	return str::rstrip(str::rstrip(parent), SEP) + SEP + str::lstrip(str::rstrip(child), SEP);
}

std::vector<findres> find(const std::string &path, const char* spec/* = "*"*/, file::attribute attrib/* = file::attribute::ALL*/, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	std::vector<findres> results;
	struct _finddata_t fdata;
	intptr_t hd = 0;

	std::string paths = mkpath(path, spec);
	if ((hd = _findfirst(paths.c_str(), &fdata)) != -1) {
		do {
			if ((attrib == file::attribute::ALL || (fdata.attrib & (unsigned)attrib) != 0) && (onlyvisible && *fdata.name != '.')) {
				if (onlyname) {
					results.push_back(findres(fdata.name, fdata.size, fdata.time_create, fdata.time_access, fdata.time_write, fdata.attrib));
				} else {
					results.push_back(findres(mkpath(path, fdata.name).c_str(), fdata.size, fdata.time_create, fdata.time_access, fdata.time_write, fdata.attrib));
				}
			}
		} while (_findnext(hd, &fdata) == 0);
		_findclose(hd);
	}

	return results;
}

std::vector<std::string> finds(const std::string &path, const char* spec/* = "*"*/, file::attribute attrib/* = attrib::ALL*/, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	std::vector<std::string> results;
	struct _finddata_t fdata;
	intptr_t hd = 0;

	std::string paths = mkpath(path, spec);
	if ((hd = _findfirst(paths.c_str(), &fdata)) != -1) {
		do {
			if ((attrib == file::attribute::ALL || (fdata.attrib & (unsigned)attrib) != 0) && (onlyvisible && *fdata.name != '.')) {
				if (onlyname) {
					results.push_back(fdata.name);
				} else {
					results.push_back(mkpath(path, fdata.name));
				}
			}
		} while (_findnext(hd, &fdata) == 0);
		_findclose(hd);
	}
	return results;
}

std::vector<std::string> dirs(const std::string &path, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	return finds(path, "*", file::attribute::DIR, onlyvisible, onlyname);
}

std::vector<std::string> files(const std::string &path, bool onlyvisible/* = true*/, bool onlyname/* = true*/) {
	return finds(path, "*", file::attribute::FILE, onlyvisible, onlyname);
}
END_CUBE_SYS_PATH_NS
