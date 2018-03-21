#include <time.h>
#include "cube\sys\time.h"
BEGIN_CUBE_SYS_TIME_NS
int now(timeunit u, timezone tz) {
	struct tm *tt = now(tz);
	switch (u) {
	case timeunit::year:
		return tt->tm_year + 1900;
		break;
	case timeunit::month:
		return tt->tm_mon + 1;
		break;
	case timeunit::day:
	case timeunit::mday:
		return tt->tm_mday;
		break;
	case timeunit::hour:
		return tt->tm_hour;
		break;
	case timeunit::min:
		return tt->tm_min;
		break;
	case timeunit::sec:
		return tt->tm_sec;
		break;
	case timeunit::week:
	case timeunit::wday:
		return tt->tm_wday + 1;
		break;
	case timeunit::yday:
		return tt->tm_yday;
		break;
	default:
		return -1;
		break;
	}
}

struct tm *now(timezone tz) {
	time_t t = ::time(0);
	switch (tz) {
	case timezone::utc:
		return ::gmtime(&t);
		break;
	case timezone::local:
		return ::localtime(&t);
		break;
	default:
		return 0;
		break;
	}
}

std::string now(const char* format, timezone tz) {
	struct tm *tt = now(tz);

	const int bufsz = 128;
	char buf[bufsz] = { 0 };
	strftime(buf, bufsz - 1, format, tt);
	return std::string(buf);
}

std::string gmt(::time_t t) {
	struct tm *tm = ::gmtime(&t);
	const int bufsz = 128;
	char buf[bufsz] = { 0 };
	strftime(buf, bufsz - 1, "%a, %d %b %Y %T GMT", tm);
	return std::string(buf);
}
END_CUBE_SYS_TIME_NS
