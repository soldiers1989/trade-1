"""
    table class
"""
from .series import Series


class Table:
    """
        base class of models
    """
    def __init__(self, data, index=None, columns=None):
        """
            initialize table with table data
        :param data: array, data frame of table
        :param index: array, index values of table rows
        :param columns: array, column names of table
        """
        self._data, self._index = {}, {}
        if isinstance(data, list) or isinstance(data, tuple): # input data is list
            if len(data) > 0:
                # detect the row and column number
                rownum, colnum = None, None
                if isinstance(data[0], list) or isinstance(data[0], tuple):
                    colnum = len(data)
                    for col in data:
                        if rownum is None:
                            rownum = len(col)
                        else:
                            if rownum < len(col):
                                rownum = len(col)
                else:
                    colnum = 1
                    rownum = len(data)

                # construct index, make sure index is satisfied with data
                if index is not None:
                    if len(index) != rownum:
                        raise ValueError("table index values is not satisfied.")
                    for i in range(0, rownum):
                        self._index[index[i]] = i
                else:
                    for i in range(0, rownum):
                        self._index[i] = i

                # construct columns, make sure columns is satisfied with data
                if columns is not None:
                    if len(columns) != colnum:
                        raise ValueError("table column names is not satisfied.")

                else:
                    columns = [i for i in range(0, colnum)]

                # construct table data
                if colnum == 1:
                    self._data[columns[0]] = data
                else:
                    for i in range(0, colnum):
                        self._data[columns[i]] = data[i]
        elif isinstance(data, dict): # input data dict
            if len(data) > 0:
                # detect the row and column number
                rownum, columns = None, len(data)
                for col in data.values():
                    if rownum is None:
                        rownum = len(col)
                    else:
                        if rownum < len(col):
                            rownum = len(col)

                # construct index, make sure index is satisfied with data
                if index is not None:
                    if len(index) != rownum:
                        raise ValueError("table index values is not satisfied.")
                    for i in range(0, rownum):
                        self._index[index[i]] = i
                else:
                    for i in range(0, rownum):
                        self._index[i] = i

                # construct table data
                self._data = data
        else:
            raise ValueError("table data must be list|tupe|dict.")

    def __getitem__(self, column):
        data = self._data.get(column, None)
        if data is not None:
            Series(data.extend([None]*(len(self._index)-len(data))), self._index)
        return data

    def __setitem__(self, column, value):
        if value is None:
            self._data.pop(column, None)
        else:
            if isinstance(value, list):
                self._data[column] = value
            elif isinstance(value, tuple):
                self._data[column] = list(value)
            else:
                raise ValueError("table column data is not satisfied.")

    @property
    def data(self):
        return list(self._data.values())

    @property
    def columns(self):
        pass

    @columns.setter
    def columns(self, cols):
        pass

    @property
    def index(self):
        pass

    @index.setter
    def index(self, idxs):
        pass
