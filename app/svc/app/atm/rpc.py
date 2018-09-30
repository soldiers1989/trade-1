"""
    rpc object
"""
from trpc import aam, quote, trade

AamStockRpc = aam.stock.StockRpc
AamOrderRpc = aam.order.OrderRpc
AamTradeRpc = aam.trade.TradeRpc

QuoteRpc = quote.QuoteRpc

TradeRpc = trade.TradeRpc
