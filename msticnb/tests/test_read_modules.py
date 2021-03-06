# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""read_modules test class."""
from pathlib import Path
import unittest

from ..read_modules import discover_modules, Notebooklet, find, nblts, nb_index
from .unit_test_lib import TEST_DATA_PATH


class TestReadModules(unittest.TestCase):
    """Unit test class."""

    def test_read_modules(self):
        """Test method."""
        nbklts = discover_modules()
        self.assertGreaterEqual(len(list(nbklts.iter_classes())), 4)

        # pylint: disable=no-member
        match, m_count = nblts.azsent.host.HostSummary.match_terms("host, linux, azure")
        self.assertTrue(match)
        self.assertEqual(m_count, 3)

        for key, value in nbklts.iter_classes():
            self.assertIsInstance(key, str)
            self.assertTrue(issubclass(value, Notebooklet))

        find_res = find("host windows azure")
        self.assertGreater(len(find_res), 0)
        not_found = find("monkey stew")
        self.assertEqual(len(not_found), 0)

    def test_read_custom_path(self):
        """Test method."""
        cust_nb_path = Path(TEST_DATA_PATH) / "custom_nb"
        nbklts = discover_modules(nb_path=str(cust_nb_path))
        self.assertGreaterEqual(len(list(nbklts.iter_classes())), 5)

        # pylint: disable=no-member
        match, m_count = nblts.custom_nb.host.CustomNB.match_terms("Custom")
        self.assertTrue(match)
        self.assertEqual(m_count, 1)

        for key, value in nbklts.iter_classes():
            self.assertIsInstance(key, str)
            self.assertTrue(issubclass(value, Notebooklet))

        find_res = find("banana")
        self.assertEqual(len(find_res), 1)
        find_res = find("<<Test Marker>>")
        self.assertEqual(len(find_res), 1)
        self.assertEqual(find_res[0][0], "CustomNB")
        self.assertIn("nblts.host.CustomNB", nb_index)
