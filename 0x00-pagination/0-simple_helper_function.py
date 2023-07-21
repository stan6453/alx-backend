#!/usr/bin/env python3
"""
Pagination helper function
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    calculate the range of items to return, given a page_size
    and a page_number
    """
    end_index = page_size * page
    page_offset = page_size
    start_index = end_index - page_offset

    return start_index, end_index
