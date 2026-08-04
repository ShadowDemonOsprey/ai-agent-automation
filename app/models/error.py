"""
API error response models.

Defines the structure of errors
returned by the API.
"""


from pydantic import BaseModel



class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """


    error: str
    """
    Error category.
    """


    message: str
    """
    Detailed error message.
    """