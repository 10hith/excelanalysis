from fastapi import APIRouter

mappRouter = APIRouter(
    prefix="/mapp",
    tags=["mapp"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@mappRouter.get("/")
async def read_items():
    return fake_items_db

# mappRouter.mount("/profile-f", WSGIMiddleware(profile_f_app.server))