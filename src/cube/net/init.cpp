#include "cube\net\init.h"
#include "cube\sys\error.h"
#include <WinSock2.h>
BEGIN_CUBE_NET_NS
//for initialize the windows socket environment
static const init g_netsvc_init;

init::init() {
	/*start up windows socket environment*/
	WORD wsaversion;
	WSADATA wsadata;
	wsaversion = MAKEWORD(2, 2);

	int err = WSAStartup(wsaversion, &wsadata);
	if (err != 0) { //startup windows socket environment failed.
		throw std::exception(sys::last_error().c_str());
	}
}

init::~init() {
	/*clean the windows socket environment*/
	WSACleanup();
}
END_CUBE_NET_NS
