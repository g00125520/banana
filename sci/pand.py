from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np


def t_ser():
    s = pd.Series([1,2,3,4,5], index=['a', 'b', 'c', 'd', 'e'])
    s2 = pd.Series([10,20,30,40,50], index=['b', 'c', 'd', 'e', 'f'])
    print(s[1:3])
    print(s['a':'d'])
    print(s + s2)


def t_df():
    df1 = pd.DataFrame(np.random.randint(0, 10, (4, 2)), 
                       index = ['A', 'B', 'C', 'D'],
                       columns = ['a', 'b'])
    print(df1)

    df2 = pd.DataFrame({'a': [1,2,3,4], 'b': [5,6,7,8]},
                       index = ['A', 'B', 'C', 'D'])
    print(df2)

    arr = np.array([("item1", 1), ("item2", 2), ("item3", 3), ("item4", 4)], 
                   dtype=[("name", "10S"), ("count", int)])
    df3 = pd.DataFrame(arr)
    print(df3)

    dict1 = {'a': [1,2,3], 'b': [4,5,6]}
    dict2 = {'a': {'A':1,'B':2}, 'b':{'A':3, 'C':4}}

    df1 = pd.DataFrame.from_dict(dict1, orient="index")
    df2 = pd.DataFrame.from_dict(dict1, orient="columns")
    df3 = pd.DataFrame.from_dict(dict2)
    df4 = pd.DataFrame.from_dict(dict2, orient="index")
    print(df1)
    print(df2)
    print(df3)
    print(df4)

    #items = dict1.items()
    #df1 = pd.DataFrame.from_items(items, orient="index", columns=['a', 'b', 'c'])

    midx = pd.MultiIndex.from_product([['a', 'b', 'c'], ['x', 'y']], 
                                      names=['c1', 'c2'])
    df1 = pd.DataFrame(np.random.randint(0, 10, (6,6)), 
                       columns = midx, index = midx)
    print(df1)

def t_df2():
    import io
    
    txt = """ 
    A, B|C|D
    B, E|F
    C, A
    D, B|C
    """

    df = pd.read_csv(io.BytesIO(str.encode(txt)), skipinitialspace=True, header=None)
    print(df)
    nodes = df[1].str.split('|')
    from_node = df[0].values.repeat(nodes.str.len().astype(np.int32))
    to_node = np.concatenate(nodes)
    print(pd.DataFrame({"from_node": from_node, "to_node": to_node}))

    print(df[1].str.get_dummies(sep='|'))
    print(df[1].map(lambda s: max(s.split('|'))))

def t_time():
    
    def random_t(start, end, freq, count):
        index = pd.date_range(start, end, freq=freq)
        locations = np.random.choice(np.arange(len(index)), 
                                     size = count, 
                                     replace = False)
        locations.sort()
        return index[locations]
    
    np.random.seed(42)
    ts_index = random_t("2020-01-01", "2020-07-20", freq="Min", count=5)
    pd_index = ts_index.to_period("M")
    td_index = pd.TimedeltaIndex(np.diff(ts_index))

    print(ts_index)
    print(pd_index)
    print(td_index)

    t_series = pd.Series(range(5), index=ts_index)
    print(t_series)
    print(t_series.between_time("9:00", "18:00"))
    print(t_series.tshift(1, freq="D"))
        

if __name__ == '__main__':
    t_time()
    