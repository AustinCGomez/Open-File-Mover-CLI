import unittest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import sys

# Import the module to test (assuming the original file is named main.py)
# You'll need to save the original code as main.py first
try:
    import main
except ImportError:
    # If running as standalone, create a mock module for testing structure
    print("Warning: main module not found. Save the original code as 'main.py' first.")
    sys.exit(1)


class TestFileMover(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        self.empty_dir = os.path.join(self.test_dir, "empty")
        
        # Create directories
        os.makedirs(self.source_dir)
        os.makedirs(self.dest_dir)
        os.makedirs(self.empty_dir)
        
        # Create test files
        self.test_files = [
            "document.txt",
            "image.jpg",
            "spreadsheet.xlsx",
            "presentation.pdf",
            "archive.ZIP",  # Test uppercase extension
            "noextension"
        ]
        
        for filename in self.test_files:
            filepath = os.path.join(self.source_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"Test content for {filename}")
    
    def tearDown(self):
        """Clean up after each test."""
        shutil.rmtree(self.test_dir)
    
    def test_show_banner(self):
        """Test banner display function."""
        with patch('builtins.print') as mock_print:
            main.show_banner()
            # Check that print was called multiple times
            self.assertTrue(mock_print.called)
            # Verify banner content is printed
            calls = mock_print.call_args_list
            banner_content = ''.join(str(call) for call in calls)
            self.assertIn('Open File Mover CLI', banner_content)
    
    @patch('tkinter.filedialog.askdirectory')
    @patch('tkinter.Tk')
    def test_get_directory_success(self, mock_tk, mock_askdirectory):
        """Test successful directory selection."""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_askdirectory.return_value = "/test/path"
        
        with patch('builtins.print'):
            result = main.get_directory("Test prompt")
        
        self.assertEqual(result, "/test/path")
        mock_root.withdraw.assert_called_once()
        mock_root.destroy.assert_called_once()
    
    @patch('tkinter.filedialog.askdirectory')
    @patch('tkinter.Tk')
    @patch('sys.exit')
    def test_get_directory_no_selection(self, mock_exit, mock_tk, mock_askdirectory):
        """Test behavior when no directory is selected."""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_askdirectory.return_value = ""  # No selection
        
        with patch('builtins.print'):
            main.get_directory("Test prompt")
        
        mock_exit.assert_called_once_with(1)
    
    @patch('builtins.input', side_effect=['txt', 'pdf', 'done'])
    def test_get_extensions_normal(self, mock_input):
        """Test normal extension input."""
        with patch('builtins.print'):
            result = main.get_extensions()
        
        self.assertEqual(result, ['txt', 'pdf'])
    
    @patch('builtins.input', side_effect=['TXT', 'PDF', 'txt', 'done'])  # Test duplicates and case
    def test_get_extensions_duplicates_and_case(self, mock_input):
        """Test extension input with duplicates and case variations."""
        with patch('builtins.print'):
            result = main.get_extensions()
        
        self.assertEqual(result, ['txt', 'pdf'])  # Should be lowercase and no duplicates
    
    @patch('builtins.input', side_effect=['', '  ', 'done'])
    def test_get_extensions_empty_input(self, mock_input):
        """Test extension input with empty/whitespace entries."""
        with patch('builtins.print'):
            result = main.get_extensions()
        
        self.assertEqual(result, [])
    
    @patch('builtins.input', side_effect=['y'])
    def test_confirm_action_yes(self, mock_input):
        """Test confirmation with yes response."""
        result = main.confirm_action("Test message")
        self.assertTrue(result)
    
    @patch('builtins.input', side_effect=['n'])
    def test_confirm_action_no(self, mock_input):
        """Test confirmation with no response."""
        result = main.confirm_action("Test message")
        self.assertFalse(result)
    
    @patch('builtins.input', side_effect=['invalid', 'y'])
    def test_confirm_action_retry(self, mock_input):
        """Test confirmation with invalid input followed by valid input."""
        with patch('builtins.print'):
            result = main.confirm_action("Test message")
        self.assertTrue(result)
    
    def test_move_files_by_extension_success(self):
        """Test successful file moving by extension."""
        extensions = ['txt', 'pdf']
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, self.dest_dir, extensions
            )
        
        self.assertTrue(result)
        
        # Check that txt file was moved
        moved_file = os.path.join(self.dest_dir, "document.txt")
        self.assertTrue(os.path.exists(moved_file))
        
        # Check that txt file was removed from source
        source_file = os.path.join(self.source_dir, "document.txt")
        self.assertFalse(os.path.exists(source_file))
        
        # Check that other files remain in source
        remaining_file = os.path.join(self.source_dir, "image.jpg")
        self.assertTrue(os.path.exists(remaining_file))
    
    def test_move_files_case_insensitive_extensions(self):
        """Test that file extension matching is case-insensitive."""
        extensions = ['zip']  # lowercase
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, self.dest_dir, extensions
            )
        
        self.assertTrue(result)
        
        # Check that ZIP file was moved (case insensitive match)
        moved_file = os.path.join(self.dest_dir, "archive.ZIP")
        self.assertTrue(os.path.exists(moved_file))
    
    def test_move_files_nonexistent_source(self):
        """Test moving files with nonexistent source directory."""
        fake_source = "/nonexistent/path"
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                fake_source, self.dest_dir, ['txt']
            )
        
        self.assertFalse(result)
    
    def test_move_files_nonexistent_dest(self):
        """Test moving files with nonexistent destination directory."""
        fake_dest = "/nonexistent/path"
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, fake_dest, ['txt']
            )
        
        self.assertFalse(result)
    
    def test_move_files_no_matching_extensions(self):
        """Test moving files when no files match the extensions."""
        extensions = ['nonexistent']
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, self.dest_dir, extensions
            )
        
        self.assertTrue(result)  # Function should succeed but move 0 files
    
    def test_move_folder_success(self):
        """Test successful folder moving."""
        # Create a test folder to move
        test_folder = os.path.join(self.source_dir, "test_folder")
        os.makedirs(test_folder)
        
        # Add a file to the folder
        test_file = os.path.join(test_folder, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        with patch('builtins.print'):
            result = main.move_folder(test_folder, self.dest_dir)
        
        self.assertTrue(result)
        
        # Check that folder was moved
        moved_folder = os.path.join(self.dest_dir, "test_folder")
        self.assertTrue(os.path.exists(moved_folder))
        
        # Check that file inside folder was moved too
        moved_file = os.path.join(moved_folder, "test.txt")
        self.assertTrue(os.path.exists(moved_file))
        
        # Check that original folder no longer exists
        self.assertFalse(os.path.exists(test_folder))
    
    def test_move_folder_nonexistent_source(self):
        """Test moving nonexistent folder."""
        fake_folder = "/nonexistent/folder"
        
        with patch('builtins.print'):
            result = main.move_folder(fake_folder, self.dest_dir)
        
        self.assertFalse(result)
    
    def test_move_folder_nonexistent_dest(self):
        """Test moving folder to nonexistent destination."""
        test_folder = os.path.join(self.source_dir, "test_folder")
        os.makedirs(test_folder)
        fake_dest = "/nonexistent/destination"
        
        with patch('builtins.print'):
            result = main.move_folder(test_folder, fake_dest)
        
        self.assertFalse(result)
    
    def test_delete_permanently_file(self):
        """Test permanent deletion of a file."""
        test_file = os.path.join(self.source_dir, "to_delete.txt")
        with open(test_file, 'w') as f:
            f.write("delete me")
        
        with patch('builtins.print'):
            result = main.delete_permanently(test_file)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(test_file))
    
    def test_delete_permanently_folder(self):
        """Test permanent deletion of a folder."""
        test_folder = os.path.join(self.source_dir, "to_delete_folder")
        os.makedirs(test_folder)
        
        # Add a file to the folder
        test_file = os.path.join(test_folder, "file.txt")
        with open(test_file, 'w') as f:
            f.write("content")
        
        with patch('builtins.print'):
            result = main.delete_permanently(test_folder)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(test_folder))
    
    def test_delete_permanently_nonexistent(self):
        """Test deletion of nonexistent path."""
        fake_path = "/nonexistent/path"
        
        with patch('builtins.print'):
            result = main.delete_permanently(fake_path)
        
        self.assertFalse(result)
    
    @patch('builtins.input', side_effect=['4'])  # Exit choice
    def test_main_menu_exit(self, mock_input):
        """Test main menu exit functionality."""
        with patch('builtins.print'):
            result = main.main_menu()
        
        # Should exit gracefully without calling sys.exit
        self.assertIsNone(result)
    
    @patch('builtins.input', side_effect=['invalid', '4'])  # Invalid then exit
    def test_main_menu_invalid_choice(self, mock_input):
        """Test main menu with invalid choice."""
        with patch('builtins.print'):
            result = main.main_menu()
        
        # Should handle invalid input and then exit gracefully
        self.assertIsNone(result)
    
    def test_file_with_no_extension_handling(self):
        """Test handling of files with no extension."""
        # Test that files without extensions are not moved when looking for specific extensions
        extensions = ['txt']
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, self.dest_dir, extensions
            )
        
        self.assertTrue(result)
        
        # File with no extension should remain in source
        no_ext_file = os.path.join(self.source_dir, "noextension")
        self.assertTrue(os.path.exists(no_ext_file))
    
    @patch('shutil.move', side_effect=PermissionError("Permission denied"))
    def test_move_files_permission_error(self, mock_move):
        """Test handling of permission errors during file moving."""
        extensions = ['txt']
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, self.dest_dir, extensions
            )
        
        # Function should still return True even if individual files fail
        self.assertTrue(result)
    
    @patch('shutil.move', side_effect=PermissionError("Permission denied"))
    def test_move_folder_permission_error(self, mock_move):
        """Test handling of permission errors during folder moving."""
        test_folder = os.path.join(self.source_dir, "test_folder")
        os.makedirs(test_folder)
        
        with patch('builtins.print'):
            result = main.move_folder(test_folder, self.dest_dir)
        
        self.assertFalse(result)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for real-world scenarios."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        os.makedirs(self.source_dir)
        os.makedirs(self.dest_dir)
    
    def tearDown(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_mixed_case_extensions_scenario(self):
        """Test scenario with mixed case file extensions."""
        # Create files with various case extensions
        files = ["doc.PDF", "image.JPG", "text.txt", "archive.Zip"]
        for filename in files:
            filepath = os.path.join(self.source_dir, filename)
            with open(filepath, 'w') as f:
                f.write("content")
        
        # Test moving with lowercase extension list
        extensions = ['pdf', 'jpg']
        
        with patch('builtins.print'):
            result = main.move_files_by_extension(
                self.source_dir, self.dest_dir, extensions
            )
        
        self.assertTrue(result)
        
        # Check that both PDF and JPG files were moved regardless of case
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "doc.PDF")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "image.JPG")))
        
        # Check that other files remained
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "text.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.source_dir, "archive.Zip")))


if __name__ == '__main__':
    # Configure test runner
    unittest.main(verbosity=2, buffer=True)