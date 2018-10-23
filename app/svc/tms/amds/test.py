from tms.amds import asmd

if __name__ == '__main__':
    results = asmd.stock.get_list()
    print(len(results))
    print(results)