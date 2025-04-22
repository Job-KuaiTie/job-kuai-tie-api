from .base import router as base_router
from .account import router as account_router
from .company import router as company_router
from .job import router as job_router
# from .category import router as category_router

routers = [
    base_router,
    account_router,
    company_router,
    job_router,
]  # ,  category_router, ]
