/*
*	fd - file/directory module
*/
#pragma once
#include "cube.h"
#include <vector>
BEGIN_CUBE_NAMESPACE
//find result for find file method
typedef class findres {
public:
	findres(const char* name, int64 size, int64 create_time, int64 access_time, int64 write_time, unsigned attrib) :
		name(name), size(size), create_time(create_time), access_time(access_time), write_time(write_time), attrib(attrib) {}
	~findres() {}

	std::string name; //file name
	int64     size; //file size
	int64  create_time; // create time, -1 for FAT file systems
	int64  access_time; // last access time, -1 for FAT file systems
	int64  write_time; //last write time
	unsigned  attrib; //file attribute
} findres_t;

//file/directory class
class fd {
public:
	//seperator of path
	static const char *SEP;
	//exceptions
	typedef std::exception error;
	//file attribute
	typedef enum{FILE = 0x20, DIR=0x10, HIDDEN=0x02, SYSTEM=0x04, ALL=0xFF} attrib;
public:
	/*
	*	test if specified file or directory is exist
	*@param path: file path
	*@return:
	*	true if file exist, otherwise false
	*/
	static bool exist(const std::string &path);

	/*
	*	test if specified path represents a directory
	*@param path: file path
	*@return:
	*	true if is directory, otherwise false
	*/
	static bool isdir(const std::string &path);

	/*
	*	test if specified path represents a normal file
	*@param path: file path
	*@return:
	*	true if is normal file, otherwise false
	*/
	static bool isfile(const std::string &path);

	/*
	*	get file name from file path
	*@param path: in, file path
	*@return:
	*	file name
	*/
	static std::string name(const std::string &path);

	/*
	*	get the file's directory path from file path
	*@param path: in, file path
	*@return:
	*	file's directory path
	*/
	static std::string path(const std::string &path);

	/*
	*	find file/directory in the specified path
	*@param path: in, directory path
	*@param attrib: in, filter of file/directory attribute
	*@param onlyname: in, want only file/dir name in return results
	*@return:
	*	find results
	*/
	static std::vector<findres> find(const std::string &path, const char* spec="*", attrib = attrib::ALL, bool onlyname = true);
	static std::vector<std::string> finds(const std::string &path, const char* spec = "*", int attrib = attrib::ALL, bool onlyname = true);

	/*
	*	get the sub directories or files in the specified directory
	*@param path: in, directory path
	*@param onlyname: in, want only file/dir name in return results
	*@return:
	*	file or directory path vector
	*/
	static std::vector<std::string> dirs(const std::string &path, bool onlyname = true);
	static std::vector<std::string> files(const std::string &path, bool onlyname = true);
};

//file class
class file {
public:
	//exceptions
	typedef std::exception error;

public:
	/*
	*	read all content of file by specified file path
	*@param path: in, file path
	*@param sz: out, data read in bytes
	*@return:
	*	content of file or 0 if read file failed.
	*/
	static char* read(const std::string &path, int &sz);

	/*
	*	write content to specified file, replace file if exists
	*@param path: in, file path
	*@param content: in, content want to write
	*@param sz: in, size of content in byte
	*@return:
	*	0 for success, otherwise <0
	*/
	static int write(const std::string &path, const char* content, int sz);
};

//directory class
class dir {
public:
	//exceptions
	typedef std::exception error;

public:
	/*
	*	make directory by specified directory path
	*@param path: directory path
	*@return:
	*	0 for success, otherwise <0
	*/
	static int mkdir(const std::string &path);

	/*
	*	make directory by specified directory path, create parent directory if not exist
	*@param path: directory path
	*@return:
	*	0 for success, otherwise <0
	*/
	static int mkdirs(const std::string &path);
};
END_CUBE_NAMESPACE
