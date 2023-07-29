#!/usr/bin/env python3
"""Tests for utils.py"""

import unittest
from unittest.mock import patch, MagicMock
from utils import access_nested_map, get_json
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Test for utils.access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """Test if right output is returned"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_result):
        """Test if right errors are raised"""
        with self.assertRaises(KeyError, msg=expected_result):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("requests.get")
    def test_get_json(self,test_url, test_payload, mock_get):
        """Mock get network request"""
        get_return_value = MagicMock()
        get_return_value.json.return_value = test_payload
        mock_get.return_value = get_return_value

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

