"""Custom error handlers and exception middleware for FastAPI."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class ErrorResponse:
    """Standard error response format."""
    
    @staticmethod
    def format_error(
        error_code: str,
        message: str,
        details: dict = None,
        status_code: int = 500
    ) -> dict:
        """
        Format error response consistently.
        
        Args:
            error_code: Machine-readable error code
            message: Human-readable error message
            details: Additional error details
            status_code: HTTP status code
            
        Returns:
            Formatted error dictionary
        """
        response = {
            "error": {
                "code": error_code,
                "message": message,
                "status": status_code
            }
        }
        
        if details:
            response["error"]["details"] = details
        
        return response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.
    
    Returns user-friendly messages for validation failures.
    """
    errors = exc.errors()
    
    # Extract field names and error messages
    field_errors = {}
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        field_errors[field] = error["msg"]
    
    logger.warning(f"Validation error on {request.url.path}: {field_errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse.format_error(
            error_code="VALIDATION_ERROR",
            message="Invalid input data",
            details={"fields": field_errors},
            status_code=422
        )
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions.
    
    Provides consistent error format for all HTTP errors.
    """
    logger.warning(f"HTTP {exc.status_code} on {request.url.path}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse.format_error(
            error_code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            status_code=exc.status_code
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions.
    
    Logs the full error and returns a safe message to the user.
    """
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse.format_error(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
            status_code=500
        )
    )


def register_error_handlers(app):
    """
    Register all custom error handlers with the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


