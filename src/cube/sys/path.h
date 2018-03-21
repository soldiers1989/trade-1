#pragma once
#include <vector>
#include "cube\sys\ftype.h"
BEGIN_CUBE_SYS_PATH_NS
/*
*	make directory by specified directory path
*@param path: directory path
*@return:
*	0 for success, otherwise <0
*/
int mkdir(const std::string &path);

/*
*	make directory by specified directory path, create parent directory if not exist
*@param path: directory path
*@return:
*	0 for success, otherwise <0
*/
int mkdirs(const std::string &path);

/*
*	make full path by parent and its child path
*@param parent: in, parent path
*@param child: in, child name/path
*@return:
*	full path combined by parent and child
*/
std::string mkpath(const std::string &parent, const std::string &child);

/*
*	find file/directory in the specified path
*@param path: in, directory path
*@param attrib: in, filter of file/directory attribute
*@param onlyname: in, want only file/dir name in return results
*@return:
*	find results
*/
std::vector<findres> find(const std::string &path, const char* spec = "*", file::attribute attrib = file::attribute::ALL, bool onlyvisible = true, bool onlyname = true);
std::vector<std::string> finds(const std::string &path, const char* spec = "*", file::attribute attrib = file::attribute::ALL, bool onlyvisible = true, bool onlyname = true);

/*
*	get the sub directories or files in the specified directory
*@param path: in, directory path
*@param onlyname: in, want only file/dir name in return results
*@return:
*	file or directory path vector
*/
std::vector<std::string> dirs(const std::string &path, bool onlyvisible = true, bool onlyname = true);
std::vector<std::string> files(const std::string &path, bool onlyvisible = true, bool onlyname = true);
END_CUBE_SYS_PATH_NS
