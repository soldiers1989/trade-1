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

//stock exchange id: ������ID�� �Ϻ�1������0(����֤ȯ��ͨ�˻�������2)
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

//current data category: 0-�ʽ� 1-�ɷ� 2-����ί�� 3-���ճɽ� 4-�ɳ�ί�� 5-�ɶ����� 6-������� 7-��ȯ��� 8-����֤ȯ
typedef enum class ccategory_t { zj = 0, gf = 1, drwt = 2, drcj = 3, kcwt = 4, gddm = 5, rzye = 6, rqye = 7, krzq = 8, other = -1 } ccategory_t;

//history data category: 0-��ʷί�� 1-��ʷ�ɽ� 2-���
typedef enum class hcategory_t { lswt = 0, lscj = 1, jgd = 2, other = -1 } hcategory_t;

//order category: 0���� 1����  2��������  3��ȯ����   4��ȯ��ȯ   5��ȯ����  6��ȯ��ȯ
typedef enum class ocategory_t { buy = 0, sell = 1, rzmr = 2, rqmc = 3, mqhq = 4, mqhk = 5, xqhk = 6, other = -1 } ocategory_t;

//price type: 0�Ϻ��޼�ί�� �����޼�ί�� 1(�м�ί��)���ڶԷ����ż۸�  2(�м�ί��)���ڱ������ż۸�  3(�м�ί��)���ڼ�ʱ�ɽ�ʣ�೷��  4(�м�ί��)�Ϻ��嵵����ʣ�� �����嵵����ʣ�� 5(�м�ί��)����ȫ��ɽ����� 6(�м�ί��)�Ϻ��嵵����ת�޼�
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
