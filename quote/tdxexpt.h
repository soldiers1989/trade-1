#pragma once
#include "stdqot.h"

BEGIN_QUOTE_NAMESPACE

/////////////////////////////////////////////////////////level 1/////////////////////////////////////////////////////////////////

//1.����API����TdxHqApi.dll�ļ��ĵ����������������º�����(�������麯����Ϊ�ͻ������������ѯ�����Ƿ���������)
//bool  TdxHq_Connect(char* IP, int Port, char* Result, char* ErrInfo);//����ȯ�����������
//void  TdxHq_Disconnect();//�Ͽ�������
//bool  TdxHq_GetSecurityCount(byte Market, short& Result, char* ErrInfo);//��ȡָ���г��ڵ�֤ȯ��Ŀ
//bool  TdxHq_GetSecurityList(byte Market, short Start, short& Count, char* Result, char* ErrInfo);//��ȡ�г���ָ����Χ�ڵ�����֤ȯ����
//bool  TdxHq_GetSecurityBars(byte Category, byte Market, char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);//��ȡ��ƱK��
//bool  TdxHq_GetIndexBars(byte Category, byte Market, char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);//��ȡָ��K��
//bool  TdxHq_GetMinuteTimeData(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡ��ʱͼ����
//bool  TdxHq_GetHistoryMinuteTimeData(byte Market, char* Zqdm, int date, char* Result, char* ErrInfo);//��ȡ��ʷ��ʱͼ����
//bool  TdxHq_GetTransactionData(byte Market, char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);//��ȡ��ʱ�ɽ�
//bool  TdxHq_GetHistoryTransactionData(byte Market, char* Zqdm, short Start, short& Count, int date, char* Result, char* ErrInfo);//��ȡ��ʷ��ʱ�ɽ�
//bool  TdxHq_GetSecurityQuotes(byte Market[], char* Zqdm[], short& Count, char* Result, char* ErrInfo);//��ȡ�̿��嵵����
//bool  TdxHq_GetCompanyInfoCategory(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡF10��Ϣ���
//bool  TdxHq_GetCompanyInfoContent(byte Market, char* Zqdm, char* FileName, int Start, int Length, char* Result, char* ErrInfo);//��ȡF10��Ϣ����
//bool  TdxHq_GetXDXRInfo(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡȨϢ����
//bool  TdxHq_GetFinanceInfo(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡ��������


///����ӿ�ִ�к����ʧ�ܣ����ַ���ErrInfo�����˳�����Ϣ����˵����
///����ɹ������ַ���Result�����˽������,��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���
///���ص�Result������ݶ���\n,\t�ָ��������ַ����������ѯK�����ݣ����صĽ���ַ���������

///��ʱ��\t���̼�\t���̼�\t��߼�\t��ͼ�\t�ɽ���\t�ɽ���\n
///20150519\t4.644000\t4.732000\t4.747000\t4.576000\t146667487\t683638848.000000\n
///20150520\t4.756000\t4.850000\t4.960000\t4.756000\t353161092\t1722953216.000000��

///��ô�����֮��ͨ���ָ��ַ����� ���Իָ�Ϊ���м��еı����ʽ������


//2.APIʹ������Ϊ: Ӧ�ó����ȵ���TdxHq_Connect����ͨ�������������,Ȼ��ſ��Ե��������ӿڻ�ȡ��������,Ӧ�ó���Ӧ���д��������������, �ӿ����̰߳�ȫ��
//������ߣ���������api������api�᷵���Ѿ����ߵĴ�����Ϣ��Ӧ�ó���Ӧ���ݴ˴�����Ϣ�������ӷ�������


//3.������������˵��
/// <summary>
///  ����ͨ�������������
/// </summary>
/// <param name="IP">������IP,����ȯ��ͨ���������¼���桰ͨѶ���á���ť�ڲ��</param>
/// <param name="Port">�������˿�</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall*  TdxHq_ConnectDelegate)(const char* IP, int Port, char* Result, char* ErrInfo);


/// <summary>
/// �Ͽ�ͬ������������
/// </summary>
typedef void(__stdcall* TdxHq_DisconnectDelegate)();


/// <summary>
/// ��ȡ֤ȯָ����Χ�ĵ�K������
/// </summary>
/// <param name="Category">K������, 0->5����K��    1->15����K��    2->30����K��  3->1СʱK��    4->��K��  5->��K��  6->��K��  7->1����  8->1����K��  9->��K��  10->��K��  11->��K��< / param>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ�Ŀ�ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ�Ĵ�С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ, ���ֵ800</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetSecurityBarsDelegate)(byte Category, byte Market, const char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ�г�������֤ȯ������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��ص�֤ȯ����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetSecurityCountDelegate)(byte Market, short& Result, char* ErrInfo);


/// <summary>
/// ��ȡ�г���ĳ����Χ�ڵ�1000֧��Ʊ�Ĺ�Ʊ����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Start">��Χ��ʼλ��,��һ����Ʊ��0, �ڶ�����1, ��������,λ����Ϣ����TdxHq_GetSecurityCount���ص�֤ȯ����ȷ��</param>
/// <param name="Count">��Χ�Ĵ�С��APIִ�к�,������ʵ�ʷ��صĹ�Ʊ��Ŀ,</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��ص�֤ȯ������Ϣ,��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetSecurityListDelegate)(byte Market, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡָ����ָ����Χ��K������
/// </summary>
/// <param name="Category">K������, 0->5����K��    1->15����K��    2->30����K��  3->1СʱK��    4->��K��  5->��K��  6->��K��  7->1����  8->1����K��  9->��K��  10->��K��  11->��K��< / param>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ�Ĵ�С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ,���ֵ800</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetIndexBarsDelegate)(byte Category, byte Market, const char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʱ����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetMinuteTimeDataDelegate)(byte Market, const char* Zqdm, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʷ��ʱ����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Date">����, ����2014��1��1��Ϊ����20140101</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetHistoryMinuteTimeDataDelegate)(byte Market, const char* Zqdm, int Date, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʱ�ɽ�ĳ����Χ�ڵ�����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetTransactionDataDelegate) (byte Market, const char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʷ��ʱ�ɽ�ĳ����Χ�ڵ�����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ</param>
/// <param name="Date">����, ����2014��1��1��Ϊ����20140101</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetHistoryTransactionDataDelegate) (byte Market, const char* Zqdm, short Start, short& Count, int Date, char* Result, char* ErrInfo);


/// <summary>
/// ������ȡ���֤ȯ���嵵��������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�, ��i��Ԫ�ر�ʾ��i��֤ȯ���г�����</param>
/// <param name="Zqdm">֤ȯ����, Count��֤ȯ������ɵ�����</param>
/// <param name="Count">APIִ��ǰ,��ʾ�û�Ҫ�����֤ȯ��Ŀ,���50(��ͬȯ�̿��ܲ�һ��,������Ŀ��������ѯȯ�̻����), APIִ�к�,������ʵ�ʷ��ص���Ŀ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetSecurityQuotesDelegate) (byte Market[], const char* Zqdm[], short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡF10���ϵķ���
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetCompanyInfoCategoryDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡF10���ϵ�ĳһ���������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="FileName">��Ŀ���ļ���, ��TdxHq_GetCompanyInfoCategory������Ϣ�л�ȡ</param>
/// <param name="Start">��Ŀ�Ŀ�ʼλ��, ��TdxHq_GetCompanyInfoCategory������Ϣ�л�ȡ</param>
/// <param name="Length">��Ŀ�ĳ���, ��TdxHq_GetCompanyInfoCategory������Ϣ�л�ȡ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����,����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetCompanyInfoContentDelegate) (byte Market, const char* Zqdm, const char* FileName, int Start, int Length, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��Ȩ��Ϣ��Ϣ
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����,����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetXDXRInfoDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ������Ϣ
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����,����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxHq_GetFinanceInfoDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);


/////////////////////////////////////////////////////////level 2/////////////////////////////////////////////////////////////////

//1.����API����TdxHqApi.dll�ļ��ĵ����������������º�����(�������麯����Ϊ�ͻ������������ѯ�����Ƿ���������)

//bool TdxL2Hq_GetDetailTransactionData(byte Market, char* Zqdm, int Start, short& Count, char* Result, char* ErrInfo);//��ȡ��ʳɽ�
//bool TdxL2Hq_GetDetailOrderData(byte Market, char* Zqdm, int Start, short& Count, char* Result, char* ErrInfo);//��ȡ���ί��
//bool TdxL2Hq_GetSecurityQuotes10 (byte Market[], char* Zqdm[], short& Count, char* Result, char* ErrInfo);//��ȡʮ������
//bool TdxL2Hq_GetBuySellQueue(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡ��������

//bool  TdxL2Hq_Connect(char* IP, int Port, char* Result, char* ErrInfo);//����ȯ�����������
//void  TdxL2Hq_Disconnect();//�Ͽ�������
//bool  TdxL2Hq_GetSecurityCount(byte Market, short& Result, char* ErrInfo);//��ȡ�г�������֤ȯ����Ŀ
//bool  TdxL2Hq_GetSecurityList(byte Market, short Start, short& Count, char* Result, char* ErrInfo);//��ȡָ����Χ�����е�֤ȯ����
//bool  TdxL2Hq_GetSecurityBars(byte Category, byte Market, char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);//��ȡ��ƱK��
//bool  TdxL2Hq_GetIndexBars(byte Category, byte Market, char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);//��ȡָ��K��
//bool  TdxL2Hq_GetMinuteTimeData(byte Market,  char* Zqdm, char* Result, char* ErrInfo);//��ȡ��ʱͼ����
//bool  TdxL2Hq_GetHistoryMinuteTimeData(byte Market, char* Zqdm, int date, char* Result, char* ErrInfo);//��ȡ��ʷ��ʱͼ����
//bool  TdxL2Hq_GetTransactionData(byte Market, char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);//��ȡ��ʱ�ɽ�
//bool  TdxL2Hq_GetHistoryTransactionData(byte Market, char* Zqdm, short Start, short& Count, int date, char* Result, char* ErrInfo);//��ȡ��ʷ��ʱ�ɽ�
//bool  TdxL2Hq_GetSecurityQuotes(byte Market[], char* Zqdm[], short& Count, char* Result, char* ErrInfo);//��ȡ�̿��嵵����
//bool  TdxL2Hq_GetCompanyInfoCategory(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡF10��Ϣ���
//bool  TdxL2Hq_GetCompanyInfoContent(byte Market, char* Zqdm, char* FileName, int Start, int Length, char* Result, char* ErrInfo);//��ȡF10��Ϣ����
//bool  TdxL2Hq_GetXDXRInfo(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡȨϢ����
//bool  TdxL2Hq_GetFinanceInfo(byte Market, char* Zqdm, char* Result, char* ErrInfo);//��ȡ������Ϣ


///����ӿ�ִ�к����ʧ�ܣ����ַ���ErrInfo�����˳�����Ϣ����˵����
///����ɹ������ַ���Result�����˽������,��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���
///���ص�Result������ݶ���\n,\t�ָ��������ַ����������ѯK�����ݣ����صĽ���ַ���������

///��ʱ��\t���̼�\t���̼�\t��߼�\t��ͼ�\t�ɽ���\t�ɽ���\n
///20150519\t4.644000\t4.732000\t4.747000\t4.576000\t146667487\t683638848.000000\n
///20150520\t4.756000\t4.850000\t4.960000\t4.756000\t353161092\t1722953216.000000��

///��ô�����֮��ͨ���ָ��ַ����� ���Իָ�Ϊ���м��еı����ʽ������


//2.APIʹ������Ϊ: Ӧ�ó����ȵ���TdxL2Hq_Connect����ͨ�������������,Ȼ��ſ��Ե��������ӿڻ�ȡ��������,Ӧ�ó���Ӧ���д��������������, �ӿ����̰߳�ȫ��
//������ߣ���������api������api�᷵���Ѿ����ߵĴ�����Ϣ��Ӧ�ó���Ӧ���ݴ˴�����Ϣ�������ӷ�������


//3.������������˵��

/// <summary>
/// ��ȡ��ʳɽ�ĳ����Χ�ڵ�����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ,���2000</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetDetailTransactionDataDelegate) (byte Market, const char* Zqdm, int Start, short& Count, char* Result, char* ErrInfo);




/// <summary>
/// ��ȡ�������ί��ĳ����Χ�ڵ�����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ,���2000</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetDetailOrderDataDelegate) (byte Market, const char* Zqdm, int Start, short& Count, char* Result, char* ErrInfo);

/// <summary>
/// ������ȡ���֤ȯ��ʮ����������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�, ��i��Ԫ�ر�ʾ��i��֤ȯ���г�����</param>
/// <param name="Zqdm">֤ȯ����, Count��֤ȯ������ɵ�����</param>
/// <param name="Count">APIִ��ǰ,��ʾ�û�Ҫ�����֤ȯ��Ŀ,���50, APIִ�к�,������ʵ�ʷ��ص���Ŀ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetSecurityQuotes10Delegate) (byte Market[], const char* Zqdm[], short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ������������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetBuySellQueueDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);




/// <summary>
///  ����ͨ�������������
/// </summary>
/// <param name="IP">������IP,������ʾ���ڲ��</param>
/// <param name="Port">�������˿�</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall*  TdxL2Hq_ConnectDelegate)(const char* IP, int Port, char* Result, char* ErrInfo);


/// <summary>
/// �Ͽ�ͬ������������
/// </summary>
typedef void(__stdcall* TdxL2Hq_DisconnectDelegate)();

/// <summary>
/// ��ȡ�г�������֤ȯ������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��ص�֤ȯ����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetSecurityCountDelegate)(byte Market, short& Result, char* ErrInfo);


/// <summary>
/// ��ȡ�г���ĳ����Χ�ڵ�1000֧��Ʊ�Ĺ�Ʊ����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Start">��Χ��ʼλ��,��һ����Ʊ��0, �ڶ�����1, ��������,λ����Ϣ����TdxL2Hq_GetSecurityCount���ص�֤ȯ����ȷ��</param>
/// <param name="Count">��Χ��С��APIִ�к�,������ʵ�ʷ��صĹ�Ʊ��Ŀ,</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��ص�֤ȯ������Ϣ,��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetSecurityListDelegate)(byte Market, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ֤ȯĳ����Χ�ڵ�K������
/// </summary>
/// <param name="Category">K������, 0->5����K��    1->15����K��    2->30����K��  3->1СʱK��    4->��K��  5->��K��  6->��K��  7->1����  8->1����K��  9->��K��  10->��K��  11->��K��< / param>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ, ���ֵ800</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetSecurityBarsDelegate)(byte Category, byte Market, const char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡָ��ĳ����Χ�ڵ�K������
/// </summary>
/// <param name="Category">K������, 0->5����K��    1->15����K��    2->30����K��  3->1СʱK��    4->��K��  5->��K��  6->��K��  7->1����  8->1����K��  9->��K��  10->��K��  11->��K��< / param>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ,���ֵ800</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetIndexBarsDelegate)(byte Category, byte Market, const char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);



/// <summary>
/// ��ȡ��ʱ����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetMinuteTimeDataDelegate)(byte Market, const char* Zqdm, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʷ��ʱ����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Date">����, ����2014��1��1��Ϊ����20140101</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetHistoryMinuteTimeDataDelegate)(byte Market, const char* Zqdm, int Date, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʱ�ɽ�ĳ����Χ�ڵ�����
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��С��APIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetTransactionDataDelegate) (byte Market, const char* Zqdm, short Start, short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡ��ʷ��ʱ�ɽ�ĳ����Χ������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Start">��Χ��ʼλ��,���һ��K��λ����0, ǰһ����1, ��������</param>
/// <param name="Count">��Χ��СAPIִ��ǰ,��ʾ�û�Ҫ�����K����Ŀ, APIִ�к�,������ʵ�ʷ��ص�K����Ŀ</param>
/// <param name="Date">����, ����2014��1��1��Ϊ����20140101</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetHistoryTransactionDataDelegate) (byte Market, const char* Zqdm, short Start, short& Count, int Date, char* Result, char* ErrInfo);

/// <summary>
/// ������ȡ���֤ȯ���嵵��������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�, ��i��Ԫ�ر�ʾ��i��֤ȯ���г�����</param>
/// <param name="Zqdm">֤ȯ����, Count��֤ȯ������ɵ�����</param>
/// <param name="Count">APIִ��ǰ,��ʾ�û�Ҫ�����֤ȯ��Ŀ,���50(��ͬȯ�̿��ܲ�һ����������Ŀ��������ѯȯ�̻����), APIִ�к�,������ʵ�ʷ��ص���Ŀ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetSecurityQuotesDelegate) (byte Market[], const char* Zqdm[], short& Count, char* Result, char* ErrInfo);


/// <summary>
/// ��ȡF10���ϵķ���
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����, ��ʽΪ������ݣ�������֮��ͨ��\n�ַ��ָ������֮��ͨ��\t�ָ���һ��Ҫ����1024*1024�ֽڵĿռ䡣����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetCompanyInfoCategoryDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);




/// <summary>
/// ��ȡF10���ϵ�ĳһ���������
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="FileName">��Ŀ���ļ���, ��TdxL2Hq_GetCompanyInfoCategory������Ϣ�л�ȡ</param>
/// <param name="Start">��Ŀ�Ŀ�ʼλ��, ��TdxL2Hq_GetCompanyInfoCategory������Ϣ�л�ȡ</param>
/// <param name="Length">��Ŀ�ĳ���, ��TdxL2Hq_GetCompanyInfoCategory������Ϣ�л�ȡ</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����,����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetCompanyInfoContentDelegate) (byte Market, const char* Zqdm, const char* FileName, int Start, int Length, char* Result, char* ErrInfo);




/// <summary>
/// ��ȡ��Ȩ��Ϣ��Ϣ
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����,����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetXDXRInfoDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);



/// <summary>
/// ��ȡ������Ϣ
/// </summary>
/// <param name="Market">�г�����,   0->����     1->�Ϻ�</param>
/// <param name="Zqdm">֤ȯ����</param>
/// <param name="Result">��APIִ�з��غ�Result�ڱ����˷��صĲ�ѯ����,����ʱΪ���ַ�����</param>
/// <param name="ErrInfo">��APIִ�з��غ�������������˴�����Ϣ˵����һ��Ҫ����256�ֽڵĿռ䡣û����ʱΪ���ַ�����</param>
/// <returns>�ɹ�����true, ʧ�ܷ���false</returns>
typedef bool(__stdcall* TdxL2Hq_GetFinanceInfoDelegate) (byte Market, const char* Zqdm, char* Result, char* ErrInfo);

END_QUOTE_NAMESPACE
