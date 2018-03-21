#include "cube\str\cast.h"
#include "cube\sys\time.h"
#include "cube\http\config.h"
#include "cube\http\response.h"
BEGIN_CUBE_HTTP_NS
////////////////////////////////////////response class///////////////////////////////////////////
std::string response::pack() const {
	std::string res("");

	//pack status line
	res.append(_status.pack());
	//pack headers
	res.append(_headers.pack());

	//pack empty line
	res.append("\r\n");

	//pack entity data
	res.append(_content);

	return res;
}

int response::parse(const std::string &str) {
	return 0;
}

void response::set_status(http::status s) {
	//set status line
	_status = s;

	//set default headers
	_headers.add("Server", http::config::server);
}

void response::set_header(const std::string &name, const std::string &value) {
	_headers.set(name, value);
}

void response::add_header(const std::string &name, const std::string &value) {
	_headers.add(name, value);
}

void response::set_content(const char *data, int sz, const std::string &type, const std::string &charset) {
	//process content type
	std::string ctype = type;
	if (!charset.empty()) {
		ctype.append(";charset=");
		ctype.append(charset);
	}

	//set status line
	_status = http::status_200_ok;

	//set general header
	_headers.add("Server", http::config::server);

	//set content type
	_headers.set("Content-Type", ctype);
		
	//set content length
	_headers.set("Content-Length", cube::str::string(sz));

	//set content data
	_content.assign(data, sz);
}

void response::set_cookie(const std::string &name, const std::string &value, int maxage) {
	std::string cookie("");
	
	cookie.append(name);
	cookie.append("=");
	cookie.append(value);
	
	cookie.append(";Expires=");
	cookie.append(sys::time::gmt(::time(0) + maxage));
	
	cookie.append(";Max-Age=");
	cookie.append(str::string(maxage));

	cookie.append(";Path=/");
	
	_headers.add("Set-Cookie", cookie);
}

void response::redirect(const char *url, bool permanent) {
	//set status line
	if (permanent)
		_status = http::status_301_moved_permanently;
	else
		_status = http::status_302_found;

	//set general header
	_headers.add("Server", http::config::server);

	//set redirect location
	_headers.add("Location", url);
}
END_CUBE_HTTP_NS
