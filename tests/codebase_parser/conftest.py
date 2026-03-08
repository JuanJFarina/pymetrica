# pylint: disable=line-too-long

import pytest

from pymetrica.models import Code, Codebase


@pytest.fixture
def small_codebase_path() -> str:
    return "./tests/sample_codebases/small_codebase"


@pytest.fixture
def big_codebase_path() -> str:
    return "./tests/sample_codebases/big_codebase"


@pytest.fixture(name="small_codebase_files")
def _small_codebase_files() -> list[Code]:
    return [
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/small_codebase/sample_code.py",
            filename="sample_code.py",
            lloc_number=40,
            comments_number=1,
            code_lines=[],
            code="",
        ),
    ]


@pytest.fixture
def expected_small_codebase(small_codebase_files: list[Code]) -> Codebase:
    return Codebase(
        root_folder_path="/workspaces/pymetrica/tests/sample_codebases/small_codebase",
        root_folder_name="small_codebase",
        folders_number=0,
        files_number=1,
        lloc_number=40,
        lloc_file_ratio="40.0:1",
        comments_number=1,
        comment_lloc_ratio="1:40.0",
        classes_number=1,
        functions_number=5,
        files=small_codebase_files,
    )


@pytest.fixture(name="big_codebase_files")
def _big_codebase_files() -> list[Code]:
    return [
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/main.py",
            filename="main.py",
            lloc_number=11,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/__init__.py",
            filename="__init__.py",
            lloc_number=0,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/exception_handlers/codebase_exception.py",
            filename="codebase_exception.py",
            lloc_number=4,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/exception_handlers/__init__.py",
            filename="__init__.py",
            lloc_number=2,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/middlewares/logging_middleware.py",
            filename="logging_middleware.py",
            lloc_number=13,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/middlewares/__init__.py",
            filename="__init__.py",
            lloc_number=2,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/routes/routes.py",
            filename="routes.py",
            lloc_number=5,
            comments_number=0,
            code_lines=[],
            code="",
        ),
        Code(
            filepath="/workspaces/pymetrica/tests/sample_codebases/big_codebase/routes/__init__.py",
            filename="__init__.py",
            lloc_number=2,
            comments_number=0,
            code_lines=[],
            code="",
        ),
    ]


@pytest.fixture
def expected_big_codebase(big_codebase_files: list[Code]) -> Codebase:
    return Codebase(
        root_folder_path="/workspaces/pymetrica/tests/sample_codebases/big_codebase",
        root_folder_name="big_codebase",
        folders_number=3,
        files_number=8,
        lloc_number=39,
        lloc_file_ratio="4.9:1",
        comments_number=0,
        comment_lloc_ratio="0:39.0",
        classes_number=2,
        functions_number=3,
        files=big_codebase_files,
    )
