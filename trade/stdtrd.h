#pragma once
#include <string>
#include <vector>

#define BEGIN_TRADE_NAMESPACE namespace trade{
#define END_TRADE_NAMESPACE }

BEGIN_TRADE_NAMESPACE
typedef unsigned char byte;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;

//stock exchange id: 交易所ID， 上海1，深圳0(招商证券普通账户深圳是2)
static const char* SZSE = "0";
static const char* SHSE = "1";
static const char* ZSSZSE = "2";

static const int TDX_BATCH_LIMIT = 20;
static const int TDX_BUFFER_SIZE_RESULT = 64 * 1024;
static const int TDX_BUFFER_SIZE_ERROR = 4 * 1024;
static const char* TDX_RESULT_ROW_SEP = "\n";
static const char* TDX_RESULT_COL_SEP = "\t";

static const char* TDX_RAWDLL_PATH = "Trade.dll";
static const char* TDX_NEWDLL_PATH = "trade\\";


//table structure for holding the results for query from remote server
typedef std::vector<std::vector<std::string>> table_t;

//current data category: 0-资金 1-股份 2-当日委托 3-当日成交 4-可撤委托 5-股东代码 6-融资余额 7-融券余额 8-可融证券
typedef enum class ccategory_t { zj = 0, gf = 1, drwt = 2, drcj = 3, kcwt = 4, gddm = 5, rzye = 6, rqye = 7, krzq = 8, other = -1 } ccategory_t;

//history data category: 0-历史委托 1-历史成交 2-交割单
typedef enum class hcategory_t { lswt = 0, lscj = 1, jgd = 2, other = -1 } hcategory_t;

//order category: 0买入 1卖出  2融资买入  3融券卖出   4买券还券   5卖券还款  6现券还券
typedef enum class ocategory_t { buy = 0, sell = 1, rzmr = 2, rqmc = 3, mqhq = 4, mqhk = 5, xqhk = 6, other = -1 } ocategory_t;

//price type: 0上海限价委托 深圳限价委托 1(市价委托)深圳对方最优价格  2(市价委托)深圳本方最优价格  3(市价委托)深圳即时成交剩余撤销  4(市价委托)上海五档即成剩撤 深圳五档即成剩撤 5(市价委托)深圳全额成交或撤销 6(市价委托)上海五档即成转限价
typedef enum class pricetype_t { xjwt = 0, sjwt1 = 1, sjwt2 = 2, sjwt3 = 3, sjwt4 = 4, sjwt5 = 5, sjwt6 = 6, other = -1 } pricetype_t;

//structure for send or cancel order
class order_t {
public:
	order_t(std::string exchange_id, std::string order_no) : exchange_id(exchange_id), order_no(order_no){}

	order_t(ocategory_t c, pricetype_t t, std::string g, std::string z, float p, int ct) : category(c), type(t), gddm(g), zqdm(z), price(p), count(ct){}

	~order_t() {}

public:
	// response of send order
	std::string exchange_id;
	std::string order_no;

	// request of send order
	ocategory_t category;
	pricetype_t type;
	std::string gddm;
	std::string zqdm;
	float price;
	int count;
};
END_TRADE_NAMESPACE
