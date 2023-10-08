from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


"""
Create a FastAPI application instance with a specific title, version, and description.

Args:
    title (str): The title of the API.
    version (str): The version of the API.
    description (str): The description of the API.

Returns:
    FastAPI: The FastAPI application instance with the specified title, version, and description.
"""

app = FastAPI(title='khondominium.com.br API', version='0.0.1', description='Api v1 do khondominium.com.br')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=80,
                log_level='info')


