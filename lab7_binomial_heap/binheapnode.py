from typing import *


class BinHeapNode:
    def __init__(self, key: Any, value: Any, degree: int = 0, rt_sibling: Optional['BinHeapNode'] = None,
                 lt_child: Optional['BinHeapNode'] = None, parent: Optional['BinHeapNode'] = None) -> None:
        self.key = key
        self.value = value
        self.degree = degree
        self.rt_sibling = rt_sibling
        self.lt_child = lt_child
        self.parent = parent


def merge_equisized_trees(heap: BinHeapNode) -> BinHeapNode:
    tmp, prev = heap, None

    while tmp.rt_sibling is not None:
        if tmp.degree == tmp.rt_sibling.degree:
            rt_sibling = tmp.rt_sibling

            if tmp.key < rt_sibling.key:
                tmp.degree += 1
                rt_sibling.parent = tmp
                tmp.rt_sibling = rt_sibling.rt_sibling
                rt_sibling.rt_sibling = tmp.lt_child
                tmp.lt_child = rt_sibling
            else:
                rt_sibling.degree += 1
                tmp.parent = rt_sibling
                tmp.rt_sibling = rt_sibling.lt_child
                rt_sibling.lt_child = tmp

                if prev is not None:
                    prev.rt_sibling = rt_sibling

                tmp = rt_sibling
        else:
            if prev is None:
                heap = tmp

            prev, tmp = tmp, tmp.rt_sibling

    return heap if prev is not None else tmp


def unite_heaps(lt_heap: BinHeapNode, rt_heap: BinHeapNode) -> BinHeapNode:
    res_heap, tmp_lt, tmp_rt = (lt_heap, lt_heap.rt_sibling, rt_heap) if lt_heap.degree <= rt_heap.degree \
        else (rt_heap, lt_heap, rt_heap.rt_sibling)

    tmp_res = res_heap
    while tmp_lt is not None and tmp_rt is not None:
        if tmp_lt.degree <= tmp_rt.degree:
            tmp_res.rt_sibling = tmp_lt
            tmp_res, tmp_lt = tmp_res.rt_sibling, tmp_lt.rt_sibling
        else:
            tmp_res.rt_sibling = tmp_rt
            tmp_res, tmp_rt = tmp_res.rt_sibling, tmp_rt.rt_sibling

    if tmp_lt is not None:
        while tmp_lt is not None:
            tmp_res.rt_sibling = tmp_lt
            tmp_res, tmp_lt = tmp_res.rt_sibling, tmp_lt.rt_sibling
    else:
        while tmp_rt is not None:
            tmp_res.rt_sibling = tmp_rt
            tmp_res, tmp_rt = tmp_res.rt_sibling, tmp_rt.rt_sibling

    return res_heap


def merge(lt_heap: Optional[BinHeapNode], rt_heap: Optional[BinHeapNode]) -> BinHeapNode:
    if lt_heap is None:
        return rt_heap

    if rt_heap is None:
        return lt_heap

    united_heap = unite_heaps(lt_heap, rt_heap)
    return merge_equisized_trees(united_heap)


def min_and_prev(heap: BinHeapNode) -> Tuple[BinHeapNode, BinHeapNode]:
    tmp, minimum, prev, min_prev = heap, heap, None, None

    while tmp is not None:
        if tmp.key <= minimum.key:
            min_prev, minimum = prev, tmp
        prev, tmp = tmp, tmp.rt_sibling

    return (min_prev, minimum)


def child_heap(node: BinHeapNode) -> Optional[BinHeapNode]:
    prev, tmp = None, node.lt_child

    while tmp is not None:
        tmp.parent = None
        rt_sibling, tmp.rt_sibling = tmp.rt_sibling, prev
        prev, tmp = tmp, rt_sibling

    return prev
