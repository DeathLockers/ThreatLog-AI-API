from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"{'could_not_validate_credentials'}",
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=f"{'you_do_not_have_permissions_to_access'}",
)

login_incorrect_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"{'email_or_password_incorrect'}",
)

email_not_exists_exception = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail=f"{'the_email_is_not_registered'}",
)

token_expiration_exception = HTTPException(
    status_code=406,
    detail=f"{'token_for_email_verification_has_expired'}"
)
