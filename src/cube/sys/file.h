#pragma once
#include "cube\sys\ftype.h"
BEGIN_CUBE_SYS_FILE_NS
/*
*	test if specified file or directory is exist
*@param path: file path
*@return:
*	true if file exist, otherwise false
*/
bool exist(const std::string &path);

/*
*	test if specified path represents a directory
*@param path: file path
*@return:
*	true if is directory, otherwise false
*/
bool isdir(const std::string &path);

/*
*	test if specified path represents a normal file
*@param path: file path
*@return:
*	true if is normal file, otherwise false
*/
bool isfile(const std::string &path);

/*
*	get file stat
*@param fd: in, file descriptor
*@param path: in, file path
*@param stat: out, file stat
*@return:
*	0 for success, otherwise <0
*/
int stat(int fd, filestat &stat);
int stat(const std::string &path, filestat &stat);

/*
*	get specified file size
*@param path: in, file path
*@return:
*	size of file
*/
int size(int fd, size_t &sz);
size_t size(const std::string &path);
int size(const std::string &path, size_t &sz);

/*
*	get file extension name
*@param path: in, file name
*@return:
*	file extension name
*/
std::string ext(const std::string &name);

/*
*	get file name from file path
*@param path: in, file path
*@return:
*	file name
*/
std::string name(const std::string &path);

/*
*	get the file's directory path from file path
*@param path: in, file path
*@return:
*	file's directory path
*/
std::string path(const std::string &path);

/*
*	read all content of file by specified file path
*@param path: in, file path
*@param data: out, data in the file read
*@return:
*	0 for succcess, otherwise <0
*/
int read(const std::string &path, std::string &data);

/*
*	read all content of file by specified file path.
*NOTES:
*	do not forget free the return content memory
*@param path: in, file path
*@param sz: out, data read in bytes
*@return:
*	content of file or 0 if read file failed.
*/
char* read(const std::string &path, int &sz);

/*
*	write content to specified file, replace file if exists
*@param path: in, file path
*@param content: in, content want to write
*@param sz: in, size of content in byte
*@return:
*	0 for success, otherwise <0
*/
int write(const std::string &path, const char* content, int sz);
END_CUBE_SYS_FILE_NS
