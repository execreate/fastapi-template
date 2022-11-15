from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import session
from .config import settings


def init_supertokens(app_name: str):
    init(
        app_info=InputAppInfo(
            app_name=app_name,
            api_domain=settings.SUPERTOKENS_API_DOMAIN,
            website_domain=settings.SUPERTOKENS_WEBSITE_DOMAIN,
            api_base_path=settings.SUPERTOKENS_API_BASE_PATH,
            website_base_path=settings.SUPERTOKENS_WEBSITE_BASE_PATH,
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPERTOKENS_CONNECTION_URI,
            api_key=settings.SUPERTOKENS_API_KEY,
        ),
        recipe_list=[
            session.init(),
        ],
        framework="fastapi",
        mode="wsgi",
    )
