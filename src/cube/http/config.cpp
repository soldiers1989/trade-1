#include "cube\http\config.h"
BEGIN_CUBE_HTTP_NS
std::string config::server = "cube/1.0"; //server name/version
std::string config::domain = "localhost"; //server domain
std::string config::default_charset = "utf-8"; //server default charset
int config::max_entity_length = 8 * 1024 * 1024; //max entity length limit with 8MB

END_CUBE_HTTP_NS
