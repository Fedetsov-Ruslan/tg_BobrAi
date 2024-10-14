from fastapi import Depends, FastAPI
from app.database.orm_query import orm_get_all_logs, orm_get_user_log
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import get_async_session

app = FastAPI()


@app.get("/logs", summary="Get all logs")
async def get_all_logs(session: AsyncSession = Depends(get_async_session)):
    logs = await orm_get_all_logs(session)
    return logs.fetchall()

@app.get("/logs/{user_id}", summary="Get logs for user")
async def get_user_logs(user_id: int, session: AsyncSession = Depends(get_async_session) ):
    logs = await orm_get_user_log(session, user_id )
    return logs.fetchall()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)