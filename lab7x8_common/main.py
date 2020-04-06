from moveheaps import *


if __name__ == '__main__':
    lt, rt = BinomialHeap(), BinomialHeap()

    for i in range(30):
        lt.insert(-i, i)
        rt.insert(i, -i)

    ref_lt, ref_rt = lt[4], rt[7]
    print(list(lt._refs.items()), list(rt._refs.items()))
    nheap = move_heaps(lt, rt)
    print(len(lt), len(rt))
    print(list(lt._refs.items()), list(rt._refs.items()))

    print(len(nheap))
    print(list(nheap._refs.items()))
    nheap.decrease_key(ref_lt, -900)
    nheap.remove(ref_rt)

    print(nheap.extract_min())
    print(len(nheap))
