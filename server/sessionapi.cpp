#include "sessionapi.h"

BEGIN_SERVER_NAMESPACE

sessionapi::sessionapi(SOCKET s, cube::uint ip, cube::uint port) : session(s, ip, port)
{

}

sessionapi::~sessionapi()
{
}
END_SERVER_NAMESPACE
