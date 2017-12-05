/*
*	file - file module
*/
#pragma once
#include "cube.h"
BEGIN_CUBE_NAMESPACE
class file {
public:
	/*
	*	test if specified file or directory is exist
	*@param path: file path
	*@return:
	*	true if file exist, otherwise false
	*/
	static bool exist(std::string path);

	/*
	*	test if specified path represents a normal file
	*@param path: file path
	*@return:
	*	true if is normal file, otherwise false
	*/
	static bool isfile(std::string path);

	/*
	*	test if specified path represents a directory
	*@param path: file path
	*@return:
	*	true if is directory, otherwise false
	*/
	static bool isdir(std::string path);

	/*
	*	get file name from file path
	*@param path: in, file path
	*@return:
	*	file name
	*/
	static std::string filename(std::string path);

	/*
	*	get the file's directory path from file path
	*@param path: in, file path
	*@return:
	*	file's directory path
	*/
	static std::string dirpath(std::string path);

	/*
	*	make directory by specified directory path
	*@param path: directory path
	*@return:
	*	0 for success, otherwise <0
	*/
	static int mkdir(std::string path);

	/*
	*	make directory by specified directory path, create parent directory if not exist
	*@param path: directory path
	*@return:
	*	0 for success, otherwise <0
	*/
	static int mkdirs(std::string path);

	/*
	*	read all content of file by specified file path
	*@param path: in, file path
	*@param sz: out, data read in bytes
	*@return:
	*	content of file or 0 if read file failed.
	*/
	static char* read(std::string path, int &sz);

	/*
	*	write content to specified file, replace file if exists
	*@param path: in, file path
	*@param content: in, content want to write
	*@param sz: in, size of content in byte
	*@return:
	*	0 for success, otherwise <0
	*/
	static int write(std::string path, const char* content, int sz);
};
END_CUBE_NAMESPACE
