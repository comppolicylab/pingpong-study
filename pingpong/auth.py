from datetime import timedelta
from typing import cast

from fastapi.responses import RedirectResponse
import jwt
from jwt.exceptions import PyJWTError

from .config import config
from .now import NowFn, utcnow
from .schemas import AuthToken, SessionToken


def decode_session_token(token: str, nowfn: NowFn = utcnow) -> SessionToken:
    """Decodes the Session Token.

    Args:
        token (str): Encoded session token JWT
        nowfn (NowFn, optional): Function to get the current time. Defaults to utcnow.

    Returns:
        SessionToken: Session Token
    """
    auth_token = decode_auth_token(token, nowfn=nowfn)
    return SessionToken(**auth_token.model_dump())


def encode_auth_token(
    sub: str,
    expiry: int = 600,
    nowfn: NowFn = utcnow,
) -> str:
    """Generates the Auth Token.

    Args:
        sub (str): A user-provided string to provide as the `sub` parameter for `AuthToken` generation.
        expiry (int, optional): Expiry in seconds. Defaults to 600.
        nowfn (NowFn, optional): Function to get the current time. Defaults to utcnow.

    Returns:
        str: Auth Token
    """
    if expiry < 1:
        raise ValueError("expiry must be greater than 1 second")

    now = nowfn()
    exp = now + timedelta(seconds=expiry)
    tok = AuthToken(
        iat=int(now.timestamp()),
        exp=int(exp.timestamp()),
        sub=sub,
    )

    secret = config.auth.secret_keys[0]

    # For some reason mypy is wrong and thinks this is a bytes object. It is
    # actually a str in PyJWT:
    # https://github.com/jpadilla/pyjwt/blob/2.8.0/jwt/api_jwt.py#L52
    return cast(
        str,
        jwt.encode(
            tok.model_dump(),
            secret.key,
            algorithm=secret.algorithm,
        ),
    )


class TimeException(Exception):
    def __init__(self, detail: str = "", user_id: str = ""):
        self.user_id = user_id
        self.detail = detail


def decode_auth_token(token: str, nowfn: NowFn = utcnow) -> AuthToken:
    """Decodes the Auth Token.

    Args:
        token (str): Auth Token
        nowfn (NowFn, optional): Function to get the current time. Defaults to utcnow.

    Returns:
        AuthToken: Auth Token

    Raises:
        jwt.exceptions.PyJWTError when token is not valid
    """
    exc: PyJWTError | TimeException | None = None

    for secret in config.auth.secret_keys:
        try:
            tok = AuthToken(
                **jwt.decode(
                    token,
                    secret.key,
                    algorithms=[secret.algorithm],
                    options={
                        "verify_exp": False,
                        "verify_nbf": False,
                    },
                )
            )

            # Custom timestamp verification according to the nowfn
            now = nowfn().timestamp()
            nbf = getattr(tok, "nbf", None)
            if nbf is not None and now < nbf:
                raise TimeException(detail="Token not valid yet", user_id=tok.sub)

            exp = getattr(tok, "exp", None)
            if exp is not None and now > exp:
                raise TimeException(detail="Token expired", user_id=tok.sub)

            return tok

        except (TimeException, PyJWTError) as e:
            exc = e
            continue

    if exc is not None:
        raise exc

    # Unclear why we would get here
    raise ValueError("invalid token")


def generate_auth_link(
    user_id: int | str,
    redirect: str = "/",
    expiry: int = 600,
    nowfn: NowFn = utcnow,
    is_study: bool = False,
    is_study_admin: bool = False,
) -> str:
    """Generates the link to log in.

    Args:
        user_id (int): User ID
        redirect (str, optional): Redirect URL. Defaults to "/".

    Returns:
        str: Auth Link
    """
    tok = encode_auth_token(str(user_id), expiry=expiry, nowfn=nowfn)
    if is_study:
        if is_study_admin:
            return config.study_url(
                f"/api/study/auth/admin?token={tok}&redirect={redirect}"
            )
        else:
            return config.study_url(f"/api/study/auth?token={tok}&redirect={redirect}")
    raise ValueError("is_study must be True for study auth links")


def redirect_with_session_study(
    destination: str, user_id: str, expiry: int = 86_400 * 30, nowfn: NowFn = utcnow
):
    """Redirect to the destination with a session token."""
    session_token = encode_auth_token(user_id, expiry=expiry, nowfn=nowfn)
    response = RedirectResponse(
        config.study_url(destination) if destination.startswith("/") else destination,
        status_code=303,
    )
    response.set_cookie(
        key="study_session",
        value=session_token,
        max_age=expiry,
    )
    return response
