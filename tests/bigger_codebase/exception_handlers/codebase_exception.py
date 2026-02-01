from fastapi.responses import JSONResponse


class CodebaseException(Exception): ...


def codebase_exception_handler(exc: CodebaseException) -> JSONResponse:
    return JSONResponse({"exception": exc.__repr__})
