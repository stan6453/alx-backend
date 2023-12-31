#!/usr/bin/env python3
"""
Pagination module
"""
from typing import Tuple
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    calculate the range of items to return, given a page_size
    and a page_number
    """
    end_index = page_size * page
    page_offset = page_size
    start_index = end_index - page_offset

    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        given a page_number and a page_size,
        returns a list of items corresponding to that range
        """
        assert type(page) is int and type(page_size) is int\
            and page > 0 and page_size > 0
        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)
        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10):
        """
        Returns information on the state of the pagination
        """
        current_items = self.get_page(page, page_size)
        total_items_length = len(self.__dataset)

        """
        if next page should exist, then this should be true:
        next_page <= math.ceil((total_items_length/page_size))
        """
        total_pages = math.ceil((total_items_length/page_size))
        next_page = page+1 if page+1 <= total_pages else None

        return {
            "page_size": len(current_items),
            "page": page,
            "data": current_items,
            "next_page": next_page,
            "prev_page": page-1 if page-1 > 0 else None,
            "total_pages": total_pages,
        }
