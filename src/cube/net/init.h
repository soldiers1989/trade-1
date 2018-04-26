#pragma once
#include <WinSock2.h>
#include "cube\ns.h"
BEGIN_CUBE_NET_NS
//class for initialize windows socket everiment
class init {
public:
	init();
	virtual ~init();
};
//for initialize the windows socket environment
static const init g_netsvc_init;
END_CUBE_NET_NS

