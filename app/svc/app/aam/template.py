"""
    message template
"""

class _ItemTpl:
    def __init__(self, item, detail):
        self.item = item
        self.detail = detail


class _Bill:
    tmargin = _ItemTpl('扣保证金', '扣保证金%s元') # take margin
    rmargin = _ItemTpl('退保证金', '退保证金%s元') # return margin
    settle = _ItemTpl('交易结算', '结算金额%s元') # settlement


bill = _Bill


class _Margin:
    init = _ItemTpl('初始保证金', '初始保证金%s元')
    add = _ItemTpl('追加保证金', '追加保证金%s元')


margin = _Margin
