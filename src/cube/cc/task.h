#pragma once
#include "cube\ns.h"
BEGIN_CUBE_CC_NS
//runnable task
class task {
public:
	virtual void run() = 0;
};

END_CUBE_CC_NS
