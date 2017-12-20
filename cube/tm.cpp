#include "tm.h"
#include <time.h>
BEGIN_CUBE_NAMESPACE
int tm::now(unit u, tz timezone) {
	struct ::tm *tt = now(timezone);
	switch (u) {
	case tm::unit::year:
		return tt->tm_year + 1900;
		break;
	case tm::unit::month:
		return tt->tm_mon + 1;
		break;
	case tm::unit::day:
	case tm::unit::mday:
		return tt->tm_mday;
		break;
	case tm::unit::hour:
		return tt->tm_hour;
		break;
	case tm::unit::min:
		return tt->tm_min;
		break;
	case tm::unit::sec:
		return tt->tm_sec;
		break;
	case tm::unit::week:
	case tm::unit::wday:
		return tt->tm_wday + 1;
		break;
	case tm::unit::yday:
		return tt->tm_yday;
		break;
	default:
		return -1;
		break;
	}
}

struct ::tm *tm::now(tz timezone) {
	time_t t = ::time(0);
	switch (timezone) {
	case cube::tm::tz::utc:
		return ::gmtime(&t);
		break;
	case cube::tm::tz::local:
		return ::localtime(&t);
		break;
	default:
		return 0;
		break;
	}
}

std::string tm::now(const char* format, tz timezone) {
	struct ::tm *tt = now(timezone);

	const int bufsz = 128;
	char buf[bufsz] = {0};
	strftime(buf, bufsz - 1, format, tt);
	return std::string(buf);
}
END_CUBE_NAMESPACE
