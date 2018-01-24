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
	findres(const std::string& name, int64 size, int64 ctime, int64 atime, int64 wtime, unsigned attrib) :
		name(name), size(size), ctime(ctime), atime(atime), wtime(wtime), attrib(attrib) {}
	~findres() {}

	std::string name; //file name
	int64  size; //file size
	int64  ctime; // create time, -1 for FAT file systems
	int64  atime; // last access time, -1 for FAT file systems
	int64  wtime; //last write time
	unsigned  attrib; //file attribute
} findres_t;

//file stat results
typedef class filestat {
public:
	filestat() {}
	filestat(ushort mode, int64 size, int64 ctime, int64 atime, int64 wtime) : 
		mode(mode), size(size), ctime(ctime), atime(atime), mtime(mtime) {}
	~filestat() {}

	ushort mode; //file mode
	int64   size; //file size
	int64	ctime; // create time
	int64	atime; // last access time
	int64	mtime; //last modify time
} filestat_t;

//file/directory class
class fd {
	//exceptions
	typedef cexception error;

public:
	//seperator of path
	static const char *SEP;
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
	*	get file stat
	*@param fd: in, file descriptor
	*@param path: in, file path
	*@param stat: out, file stat
	*@return:
	*	0 for success, otherwise <0
	*/
	static int stat(int fd, filestat &stat);
	static int stat(const std::string &path, filestat &stat);

	/*
	*	get specified file size
	*@param path: in, file path
	*@return:
	*	size of file
	*/
	static int size(int fd, size_t &sz);
	static size_t size(const std::string &path);
	static int size(const std::string &path, size_t &sz);

	/*
	*	get file extension name
	*@param path: in, file name
	*@return:
	*	file extension name
	*/
	static std::string ext(const std::string &name);

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
	static std::vector<findres> find(const std::string &path, const char* spec = "*", int attrib = attrib::ALL, bool onlyvisible = true, bool onlyname = true);
	static std::vector<std::string> finds(const std::string &path, const char* spec = "*", int attrib = attrib::ALL, bool onlyvisible = true, bool onlyname = true);

	/*
	*	get the sub directories or files in the specified directory
	*@param path: in, directory path
	*@param onlyname: in, want only file/dir name in return results
	*@return:
	*	file or directory path vector
	*/
	static std::vector<std::string> dirs(const std::string &path, bool onlyvisible = true, bool onlyname = true);
	static std::vector<std::string> files(const std::string &path, bool onlyvisible = true, bool onlyname = true);
};

//path class
class path {
public:
	/*
	*	make full path by parent and its child path
	*@param parent: in, parent path
	*@param child: in, child name/path
	*@return:
	*	full path combined by parent and child
	*/
	static std::string make(const std::string &parent, const std::string &child);
};

//file class
class file {
public:
	//exceptions
	typedef cexception error;

public:
	/*
	*	read all content of file by specified file path
	*@param path: in, file path
	*@param data: out, data in the file read
	*@return:
	*	0 for succcess, otherwise <0
	*/
	static int read(const std::string &path, std::string &data);

	/*
	*	read all content of file by specified file path.
	*NOTES:
	*	do not forget free the return content memory
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
	typedef cexception error;

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
