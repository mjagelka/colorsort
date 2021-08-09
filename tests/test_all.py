import logging
import unittest
import core

from unittest.mock import call, patch

class TestAll(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    @patch('os.path.isdir')
    def test_check_path(self, mock_isdir):
        mock_isdir.return_value = True
        self.assertEqual(core.check_path('folder1'), 'folder1/')
        self.assertEqual(core.check_path('folder1/'), 'folder1/')
        self.assertEqual(core.check_path(''), 'sample/')

    @patch('os.path.isdir')
    def test_check_path_wrong(self, mock_isdir):
        mock_isdir.return_value = False
        self.assertEqual(core.check_path('folder1'), 'sample/')

    @patch('cv2.imread')
    @patch('os.listdir')
    def test_collect_images(self, mock_listdir, mock_imread):
        mock_imread.side_effect = [[[[0, 0, 1]]], [[[0, 0, 2]]], None]
        mock_listdir.return_value = ['file1', 'file2', 'file3']
        result = core.collect_images('sample/')
        expected_result = {'file1': [[[0, 0, 1]]],
                           'file2': [[[0, 0, 2]]]}
        self.assertDictEqual(result, expected_result)

    def test_get_average_color(self):
        img = [[[0, 0, 0], [0, 4, 0]],
               [[8, 0, 0], [0, 0, 0]]]
        self.assertListEqual(core.get_average_color(img), [2, 1, 0])

    def test_find_best_color(self):
        color_dict = {'alpha': [0, 0, 0],
                      'beta': [10, 10, 10],
                      'gamma': [10, 0, 0],
                      'delta': [0, 10, 0],
                      'epsilon': [0, 0, 10]}
        self.assertEqual(core.find_best_color([0, 0, 2], color_dict), 'alpha')
        self.assertEqual(core.find_best_color([5, 6, 7], color_dict), 'beta')
        self.assertEqual(core.find_best_color([1, 8, 2], color_dict), 'delta')
