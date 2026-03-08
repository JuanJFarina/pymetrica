from pymetrica.codebase_parser.codebase_parser import parse_codebase
from pymetrica.models.codebase import Codebase


def test_parse_codebase(
    small_codebase_path: str,
    expected_small_codebase: Codebase,
) -> None:
    codebase = parse_codebase(small_codebase_path)
    assert codebase.root_folder_path == expected_small_codebase.root_folder_path
    assert codebase.root_folder_name == expected_small_codebase.root_folder_name
    assert codebase.folders_number == expected_small_codebase.folders_number
    assert codebase.files_number == expected_small_codebase.files_number
    assert codebase.lloc_number == expected_small_codebase.lloc_number
    assert codebase.lloc_file_ratio == expected_small_codebase.lloc_file_ratio
    assert codebase.comments_number == expected_small_codebase.comments_number
    assert codebase.comment_lloc_ratio == expected_small_codebase.comment_lloc_ratio
    assert codebase.classes_number == expected_small_codebase.classes_number
    assert codebase.functions_number == expected_small_codebase.functions_number

    assert codebase.files[0].filepath == expected_small_codebase.files[0].filepath
    assert codebase.files[0].filename == expected_small_codebase.files[0].filename
    assert codebase.files[0].lloc_number == expected_small_codebase.files[0].lloc_number
    assert (
        codebase.files[0].comments_number
        == expected_small_codebase.files[0].comments_number
    )


def test_parse_big_codebase(
    big_codebase_path: str,
    expected_big_codebase: Codebase,
) -> None:
    codebase = parse_codebase(big_codebase_path)
    assert codebase.root_folder_path == expected_big_codebase.root_folder_path
    assert codebase.root_folder_name == expected_big_codebase.root_folder_name
    assert codebase.folders_number == expected_big_codebase.folders_number
    assert codebase.files_number == expected_big_codebase.files_number
    assert codebase.lloc_number == expected_big_codebase.lloc_number
    assert codebase.lloc_file_ratio == expected_big_codebase.lloc_file_ratio
    assert codebase.comments_number == expected_big_codebase.comments_number
    assert codebase.comment_lloc_ratio == expected_big_codebase.comment_lloc_ratio
    assert codebase.classes_number == expected_big_codebase.classes_number
    assert codebase.functions_number == expected_big_codebase.functions_number

    for index, file in enumerate(codebase.files):
        assert file.filepath == expected_big_codebase.files[index].filepath
        assert file.filename == expected_big_codebase.files[index].filename
        assert file.lloc_number == expected_big_codebase.files[index].lloc_number
        assert (
            file.comments_number == expected_big_codebase.files[index].comments_number
        )
