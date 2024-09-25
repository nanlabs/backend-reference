from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}


@router.get("/test")
def test(request: Request) -> dict[str, str]:
    # return request headers
    return dict(request.headers)


@router.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
