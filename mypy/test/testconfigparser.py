import pytest
from mypy.config_parser import parse_config_file
from mypy.options import Options


@pytest.mark.parametrize(
    "config_content, expected_files, expected_exception",
    [
        # Files listed without spaces
        ("[mypy]\nfiles =file1.py,file2.py,file3.py", ["file1.py", "file2.py", "file3.py"], None),

        # Files listed with adequate space
        ("[mypy]\nfiles =file1.py, file2.py, file3.py", ["file1.py", "file2.py", "file3.py"], None),

        # Files with extra spaces
        ("[mypy]\nfiles =  file1.py ,   file2.py  ,   file3.py", ["file1.py", "file2.py", "file3.py"], None),

        # Files listed with a trailing comma
        ("[mypy]\nfiles =  file1.py, file2.py, file3.py,", ["file1.py", "file2.py", "file3.py"], None),

        # Empty files key
        ("[mypy]\nfiles =", [], None),

        # Files key with only a comma
        ("[mypy]\nfiles = ,", None, ValueError),

        # Mixed valid and invalid filenames
        ("[mypy]\nfiles = file1.py, , , file2.py", None, ValueError),

        # Files listed with multiple trailing comma
        ("[mypy]\nfiles =  file1.py, file2.py, file3.py,", None, ValueError),

        # Newlines between file entries
        ("[mypy]\nfiles = file1.py,\nfile2.py,\nfile3.py", ["file1.py", "file2.py", "file3.py"], None),
    ]
)
def test_parse_config_file(tmp_path, config_content, expected_files, expected_exception):
    """Parameterized test for parse_config_file handling various configurations."""
    config_path = tmp_path / "test_config.ini"
    config_path.write_text(config_content)

    options = Options()

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            parse_config_file(options, lambda: None, str(config_path), stdout=None, stderr=None)
        assert "Invalid config" in str(exc_info.value)
    else:
        parse_config_file(options, lambda: None, str(config_path), stdout=None, stderr=None)
        assert options.files == expected_files
