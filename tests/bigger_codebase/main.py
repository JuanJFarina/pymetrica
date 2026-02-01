import uvicorn
from fastapi import FastAPI

from .exception_handlers import CodebaseException, codebase_exception_handler
from .middlewares import logging_middleware
from .routes import router

app = FastAPI()

app.add_exception_handler(CodebaseException, codebase_exception_handler)
app.add_middleware(logging_middleware)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
