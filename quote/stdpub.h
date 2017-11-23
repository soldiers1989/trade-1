#pragma once
#include <string>
#include <vector>

#define BEGIN_QUOTE_NAMESPACE namespace quote{
#define END_QUOTE_NAMESPACE }

BEGIN_QUOTE_NAMESPACE
typedef unsigned char byte;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;

static const char* TDX_QUOTE1_DLL = "TdxHqApi.dll";
static const char* TDX_QUOTE2_DLL = "TdxL2HqApi.dll";
//static const char* TDX_QUOTE2_DLL = "TradeX.dll";

static const int TDX_BATCH_LIMIT = 20;
static const int TDX_BUFFER_SIZE_RESULT = 64 * 1024;
static const int TDX_BUFFER_SIZE_ERROR = 4 * 1024;
static const char* TDX_RESULT_ROW_SEP = "\n";
static const char* TDX_RESULT_COL_SEP = "\t";

typedef std::vector<std::vector<std::string>> table_t;

typedef enum class market_t{sz=0, sh=1}market_t;
typedef enum class kline_t{min5=0, min15=1, min30=2, hour=3, day=4, week=5, month=6, min=7, min1=8, day1=9, quarter=10, year=11}kline_t;

class security_t {
public:
	security_t(market_t market, std::string code) : market(market), code(code) {}
	~security_t() {}

public:
	market_t market;
	std::string code;
};
END_QUOTE_NAMESPACE

