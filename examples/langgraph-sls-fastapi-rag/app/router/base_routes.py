from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}


@router.get("/test")
def test(request: Request) -> dict[str, str]:
    # Return only non-sensitive headers or add access control
    safe_headers = {k: v for k, v in request.headers.items() 
                    if k.lower() not in ('authorization', 'cookie')}
    return safe_headers

@router.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

