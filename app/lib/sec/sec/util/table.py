"""
    table class, table data format:
    [
        [column1, column2, ... , columnN],
        [value11, value21, ... , valueN1],
        [value12, value22, ... , valueN2],
        ...
    ]

    you can access value21 by access table[column2][0], if there is same column name,
    you can access value by specified number of the same column like table[column:X][0]
"""


class Table:
    """
        base class of models
    """
    def __init__(self, data):
        """
            table data
        :param data:
        """
        if data is None:
            return

        if not self.is_table(data):
            raise "input data is not table format"

        self._data = data

    def __getitem__(self, idx):
        """
            get item by column name and row number identifier
        :param idx:
        :return:
        """
        try:
            # get column name and row number
            colname, colidx = idx, 0
            if isinstance(idx, slice):
                colname, colidx = idx.start, idx.stop

            idx, colnum = 0, None
            for i in range(0, len(self._data[0])):
                if colname == self._data[0][i]:
                    if idx == colidx:
                       colnum = i
                       break
                    else:
                        idx += 1

            colvals = None
            if colnum is not None:
                colvals = []
                for row in self._data[1:]:
                    colvals.append(row[colnum])

            return colvals

        except:
            return None

    @property
    def data(self):
        """
            get table data
        :return:
        """
        return self._data


    @staticmethod
    def is_table(data):
        """
            check data
        :param data:
        :return:
        """
        if not isinstance(data, list):
            return False

        if len(data) > 0:
            for item in data:
                if not isinstance(item, list):
                    return False

            cols = len(data[0])
            for item in data[1:]:
                if len(item) != cols:
                    return False

        return True

    @staticmethod
    def sub(data, alias):
        """
            extract columns by column name alias
        :param data: in, table
        :param alias: in, dict<alias name, [column names]>
        :return:
            sub table by extract columns with alias
        """
        if not data or not _Table.is_table(data):
            raise "input data is not table"

        if not alias:
            return data

        if not isinstance(alias, dict):
            raise "input alias is not dict"

        colnames, colnums = [], []
        for i in range(0, len(data[0])):
            for aliasname, names in alias.items():
                if data[0][i] in names:
                    colnames.append(aliasname)
                    colnums.append(i)

        result = [colnames]
        for row in data[1:]:
            newrow = []
            for num in colnums:
                newrow.append(row[num])
            result.append(newrow)

        return result


    @staticmethod
    def transform(data):
        """
            row column transform
        :param data:
        :return:
        """
        if not data or not Table.is_table(data):
            raise "input data is not table"

        result = []
        for i in range(0, len(data[0])):
            result.append([])
            for row in data:
                result[i].append(row[i])

        return result
