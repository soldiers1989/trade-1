#include "trade.h"
#include "tdx.h"
BEGIN_TRADE_NAMESPACE
char* exchange::SHENZHEN = "0"; 
char* exchange::SHANGHAI = "1";
char* exchange::SHENZHENZS = "2";

//current selected channel
trade::channel trade::_channel = channel::tdx;

//select trading channel
void trade::select(channel chnl) {
	_channel = chnl;
}

//create a new trade object
trade * trade::create() {
	switch (_channel) {
	case channel::tdx:
		return new tdx();
		break;
	default:
		return 0;
		break;
	}
}
END_TRADE_NAMESPACE
