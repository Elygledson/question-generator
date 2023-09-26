from pymongo.errors import ServerSelectionTimeoutError
from config.environment import CONFIG

import motor.motor_asyncio


class MongoDB:
    def __init__(self, db_name, collection_name):
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                CONFIG.get('MONGODB_URI'), serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print('Connected to MongoDB')
        except ServerSelectionTimeoutError:
            raise ConnectionError("Failed to connect to the MongoDB server.")

    async def find(self):
        return self.collection.find({}).to_list(None)

    async def save(self, item_data):
        item_data_dict = item_data.dict()
        await self.collection.insert_many(item_data_dict['questions'])


db = MongoDB(db_name=CONFIG.get('DB_NAME'),
             collection_name=CONFIG.get('COLLECTION'))
