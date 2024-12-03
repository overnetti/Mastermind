from fastapi import HTTPException
from sqlalchemy.future import select
from api.database.schema.DatabaseSchema import sessionLocal, UsersTable
import logging
import traceback


class PlayerLoginDatabaseService:
    def __init__(self, PlayerLoginService):
        self.playerLoginService = PlayerLoginService

    async def validateUserSignIn(self, username: str, password: str):
        async with sessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(UsersTable).where(UsersTable.username == username))
                user = result.scalars().first()

                if not user or not await self.playerLoginService.verifyPassword(password, user.password):
                    logging.error(f"Error validating user: {traceback.format_exc()}")
                    raise HTTPException(status_code=400, detail='Invalid username or password.')

                self.playerLoginService.player.userId = user.userId
                self.playerLoginService.player.username = username
