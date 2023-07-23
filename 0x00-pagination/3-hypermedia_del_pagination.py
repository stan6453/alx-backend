#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initialize the Server
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        returns metadata for the pagination state
        """
        indexed_dataset = self.indexed_dataset()
        last_index = list(indexed_dataset.keys())[-1]
        assert index >= 0 and index <= last_index

        # Get the list of all indexed_dataset keys
        # note that deleted indexes wont be part of these keys
        dataset_keys = list(indexed_dataset.keys())

        """
        store the target index in temp_index.
        since the target index might have been deleted,
        keep increasing the index till you get to an index that exits,
        or you hit the end of the dataset, at which point you stop searching.
        """
        temp_index = index
        while True:
            try:
                # try to get an index
                target_index = dataset_keys.index(temp_index)
                # exit if successful
                break
            except Exception:
                # increase temp_index to the next index to search for
                temp_index = temp_index + 1
                # exit if end of indexed_dataset
                if temp_index > last_index:
                    break

        """
        use the index you found to slice the keys of indexed_dataset
        to include only existing keys within the page_size boundary
        i.e get items from target_index to target_index + page_size
        """
        dataset_keys = dataset_keys[target_index:target_index+page_size]

        return {
            "index": index if index and index <= last_index else 0,
            "next_index": temp_index + page_size
            if temp_index + page_size < len(indexed_dataset.keys()) else 0,
            "page_size": page_size if
            last_index - index > page_size else last_index - index,
            "data": [indexed_dataset[i] for i in dataset_keys]
        }
