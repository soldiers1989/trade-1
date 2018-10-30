import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(300):
            time.sleep(1)
            #ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def test_ws():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://w.sinajs.cn/wskt?list=sz000001,sh601066",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    #test_ws()
    from tms.mds.smd import src
    #print(src.stock.get_quote(zqdm='000001,000725'))
    #results = src.stock.get_ticks(zqdm='000001', date='2018-10-24')
    results = src.stock.get_kline(zqdm='000001', type='5')
    print(results)