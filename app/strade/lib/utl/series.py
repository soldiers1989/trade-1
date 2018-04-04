"""
    series strutrue
"""


class Series:
    def __init__(self, data, index=None):
        """
            initialize series with data
        :param data: array or dict, data of series
        :param index: array, index of series data
        """
        self._data = {}
        if isinstance(data, list) or isinstance(data, tuple):
            if index is None:
                for i in range(0, len(data)):
                    self._data[i] = [data[i]]
            else:
                if isinstance(index, list) or isinstance(index, tuple):
                    if len(data) != len(index):
                        raise ValueError("series's index must be has same size with series data.")
                    for i in range(0, len(data)):
                        key = index[i]
                        if not key in self._data:
                            self._data[key] = []
                        self._data[key].append(data[i])
                else:
                    raise ValueError("series's index must be list or tuple.")
        elif isinstance(data, dict):
            for key, val in data.items():
                self._data[key] = [val]
        else:
            raise ValueError("series need array or dict to be constructed.")

    def __getitem__(self, idx, *args):
        """
            get data by index
        :param idx: object, index value of data
        :return: object
        """
        # get item by normal key
        if not isinstance(idx, tuple):
            if not isinstance(idx, slice):
                if idx not in self._data:
                    raise KeyError(idx)
                return self._data[idx][0]
            else:
                key = idx.start


        # get item by alias keys
        for alias in idx:
            if isinstance(alias, slice):
                key = alias.start
                num = alias.stop
                if key in self._data:
                    return self._data[key][num]
            else:
                if alias in self._data:
                    return self._data[alias][0]

        # item not found
        raise KeyError(idx)

    def __setitem__(self, idx, val):
        """
            set data by index
        :param idx: object, index value
        :param val: object, data value of index
        :return:
        """
        if idx in self._data:
            self._data[idx][0] = val
        else:
            self._data[idx] = [val]

    def __iter__(self):
        return iter(self._data.values())

    def __len__(self):
        return len(self._data)

    def __str__(self):
        s = []
        for key, val in self._data.items():
            s.append("%s\t%s" % (str(key), str(val)))
        return "\n".join(s)

    __repr__ = __str__

    @property
    def index(self):
        return list(self._data.keys())

    @index.setter
    def index(self, idx):
        if not (isinstance(idx, list) or isinstance(tuple)) or len(idx) != len(self):
            raise ValueError("index is not satisfied current data.")

        data, i = {}, 0
        for val in self._data.values():
            data[idx[i]] = val
            i += 1
        self._data = data

    @property
    def data(self):
        return list(self._data.values())


if __name__ == "__main__":
    s = Series([0, 1, 2, 3], ["a", "b", "c", "d"])
    b = s["a":0]
    print(b)