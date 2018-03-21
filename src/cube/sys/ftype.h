#pragma once
#include <string>
#include "cube\ns.h"
#include "cube\type.h"
BEGIN_CUBE_SYS_PATH_NS
//find result for find file method
typedef class findres {
public:
	findres(const std::string& name, int64 size, int64 ctime, int64 atime, int64 wtime, unsigned attrib) :
		name(name), size(size), ctime(ctime), atime(atime), wtime(wtime), attrib(attrib) {
	}
	~findres() {}

	std::string name; //file name
	int64  size; //file size
	int64  ctime; // create time, -1 for FAT file systems
	int64  atime; // last access time, -1 for FAT file systems
	int64  wtime; //last write time
	unsigned  attrib; //file attribute
} findres_t;
END_CUBE_SYS_PATH_NS

BEGIN_CUBE_SYS_FILE_NS
//file attribute
enum class attribute{ FILE = 0x20, DIR = 0x10, HIDDEN = 0x02, SYSTEM = 0x04, ALL = 0xFF };

//file stat results
typedef class filestat {
public:
	filestat() {}
	filestat(ushort mode, int64 size, int64 ctime, int64 atime, int64 wtime) :
		mode(mode), size(size), ctime(ctime), atime(atime), mtime(mtime) {
	}
	~filestat() {}

	ushort mode; //file mode
	int64   size; //file size
	int64	ctime; // create time
	int64	atime; // last access time
	int64	mtime; //last modify time
} filestat_t;
END_CUBE_SYS_FILE_NS
