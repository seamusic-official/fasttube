from run import dp as dispatcher
from handlers.create_video import create_video_router
from handlers.help import help_router
from handlers.newsletter import newsletter_router
from handlers.profile import profile_router
from handlers.security import security_router
from handlers.start import start_router
from handlers.youtube import youtube_router


def setup(dp: dispatcher):
    dp.include_router(create_video_router)
    dp.include_router(help_router)
    dp.include_router(newsletter_router)
    dp.include_router(profile_router)
    dp.include_router(security_router)
    dp.include_router(start_router)
    dp.include_router(youtube_router)