"""
    template for message
"""

class _ItemTpl:
    def __init__(self, item, detail):
        self.item = item
        self.detail = detail


class _Bill:
    margin = _ItemTpl('保证金', '扣保证金%s元')

bill = _Bill


class _TradeMargin:
    init = _ItemTpl('初始保证金', '初始保证金%s元')
    add = _ItemTpl('追加保证金', '追加保证金%s元')

trademargin = _TradeMargin