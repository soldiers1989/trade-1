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
END_QUOTE_NAMESPACE

