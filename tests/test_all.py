import logging
import unittest
import core

from unittest.mock import patch


class TestAll(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    @patch('os.path.isdir')
    def test_check_path(self, mock_isdir):
        """Test folder path being created correctly."""
        mock_isdir.return_value = True
        self.assertEqual(core.check_path('folder1'), 'folder1/')
        self.assertEqual(core.check_path('folder1/'), 'folder1/')
        self.assertEqual(core.check_path(''), 'sample/')

    @patch('os.path.isdir')
    def test_check_path_wrong(self, mock_isdir):
        """Test the use of default path for wrong path definition."""
        mock_isdir.return_value = False
        self.assertEqual(core.check_path('folder1'), 'sample/')

    @patch('cv2.imread')
    @patch('os.listdir')
    def test_collect_images(self, mock_listdir, mock_imread):
        """Test images being collected from given directory."""
        mock_imread.side_effect = [[[[0, 0, 1]]], [[[0, 0, 2]]], None]
        mock_listdir.return_value = ['file1', 'file2', 'file3']
        result = core.collect_images('sample/')
        expected_result = {'file1': [[[0, 0, 1]]],
                           'file2': [[[0, 0, 2]]]}
        self.assertDictEqual(result, expected_result)

    @patch('cv2.imread')
    @patch('core.modify_color')
    def test_generate_images(self, mock_modify, mock_imread):
        """Test images being created from a prototype."""
        mock_modify.return_value = 2
        result = core.generate_images('', 'file1', 2)
        mock_imread.assert_called_with('sample/file1')
        self.assertDictEqual(result, {'copy0.jpg': 2, 'copy1.jpg': 2})

        result = core.generate_images('sample/', '', 2)
        mock_imread.assert_called_with('sample/yellow-780x400.jpg')

    def test_modify_color(self):
        """Test image color modification function."""
        pass

    def test_get_average_color(self):
        """Test counting the average color of image."""
        img = [[[0, 0, 0], [0, 4, 0]],
               [[8, 0, 0], [0, 0, 0]]]
        self.assertListEqual(core.get_average_color(img), [2, 1, 0])

    def create_color_dict(self):
        """Test parsing Web colors and extracting relevant values."""
        pass

    def test_find_best_color(self):
        """Test the closest basic color being found."""
        color_dict = {'alpha': [0, 0, 0],
                      'beta': [10, 10, 10],
                      'gamma': [10, 0, 0],
                      'delta': [0, 10, 0],
                      'epsilon': [0, 0, 10]}
        self.assertEqual(core.find_best_color([0, 0, 2], color_dict), 'alpha')
        self.assertEqual(core.find_best_color([5, 6, 7], color_dict), 'beta')
        self.assertEqual(core.find_best_color([1, 8, 2], color_dict), 'delta')

    def test_create_folders(self):
        """Test the directory structure with sorted images is created."""
        pass
