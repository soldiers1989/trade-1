#pragma once
#include <vector>
#include <string>

//table structure for holding the results for query from remote server
typedef std::vector<std::vector<std::string>> table_t;

//current data category: 0-资金 1-股份 2-当日委托 3-当日成交 4-可撤委托 5-股东代码 6-融资余额 7-融券余额 8-可融证券
typedef enum class ccategory_t{zj=0, gf=1, drwt=2, drcj=3, kcwt=4, gddm=5, rzye=6, rqye=7, krzq=8, other=-1} ccategory_t;

//history data category: 0-历史委托 1-历史成交 2-交割单
typedef enum class hcategory_t{lswt=0, lscj=1, jgd=2, other=-1} hcategory_t;

//order category: 0买入 1卖出  2融资买入  3融券卖出   4买券还券   5卖券还款  6现券还券
typedef enum class ocategory_t{buy=0, sell=1, rzmr=2, rqmc=3, mqhq=4, mqhk=5, xqhk=6, other=-1} ocategory_t;

//price type: 0上海限价委托 深圳限价委托 1(市价委托)深圳对方最优价格  2(市价委托)深圳本方最优价格  3(市价委托)深圳即时成交剩余撤销  4(市价委托)上海五档即成剩撤 深圳五档即成剩撤 5(市价委托)深圳全额成交或撤销 6(市价委托)上海五档即成转限价
typedef enum class price_t{xjwt=0, sjwt1=1, sjwt2=2, sjwt3=3, sjwt4=4, sjwt5=5, sjwt6=6, other=-1} price_t;

//stock exchange id: 交易所ID， 上海1，深圳0(招商证券普通账户深圳是2)
#define SZSE "0"
#define SHSE "1"
#define ZSSZSE "2"

//order structure for send or cancel entrust
class order_t {
public:
	order_t(std::string seid, std::string orderno): seid(seid), orderno(orderno),
			category(ocategory_t::other), type(price_t::other), gddm(""), zqdm(""), price(0.0), count(0) {}
	order_t(ocategory_t c, price_t t, std::string g, std::string z, float p, int ct): category(c), type(t), gddm(g), zqdm(z), price(p), count(ct),
			seid(""), orderno("") {}
	~order_t() {}
public:
	ocategory_t category;
	price_t type;
	std::string gddm;
	std::string zqdm;
	float price;
	int count;

	std::string seid;
	std::string orderno;
};

//trader for account
class trader
{
public:
	virtual int init(std::string ip, unsigned short port, std::string version, int deptid) = 0;

	virtual int login(std::string account, std::string password, std::string &error) = 0;

	virtual int query(ccategory_t category, table_t &result, std::string &error) = 0;
	
	virtual int query(std::vector<ccategory_t> categories, std::vector<table_t> &results, std::vector<std::string> &errors) = 0;

	virtual int query(hcategory_t category, std::string start_date, std::string end_date, table_t &result, std::string &error) = 0;

	virtual int send(order_t order, table_t &result, std::string& error) = 0;

	virtual int send(ocategory_t category, price_t type, std::string gddm, std::string zqdm, float price, int count, table_t &result, std::string& error) = 0;

	virtual int send(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string> &errors) = 0;

	virtual int cancel(order_t order, table_t &result, std::string& error) = 0;

	virtual int cancel(std::string seid, std::string orderno, table_t &result, std::string& error) = 0;

	virtual int cancel(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string>& errors) = 0;

	virtual int quote(std::string stock, table_t &result, std::string& error) = 0;
	
	virtual int quote(std::vector<std::string> stocks, std::vector<table_t> &results, std::vector<std::string>& errors) = 0;

	virtual int repay(std::string amount, table_t &result, std::string& error) = 0;

	virtual int logout() = 0;

	virtual int destroy() = 0;
};

