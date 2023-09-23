import motor.motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError
from pydantic import ValidationError

from config.environment import CONFIG


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

    def question_helper(self, dic) -> dict:
        return {
            "id": str(dic["_id"]),
            "question": dic["question"],
            "options": dic["options"],
            "answer": dic["answer"],
        }

    async def find(self):
        try:
            return self.collection.find({}).to_list(None)
        except ValidationError as e:
            return str(e)

    async def save(self, item_data):
        try:
            item_data_dict = item_data.dict()
            await self.collection.insert_many(item_data_dict['questions'])
        except ValidationError as e:
            return str(e)


db = MongoDB(db_name=CONFIG.get('DB_NAME'),
             collection_name=CONFIG.get('COLLECTION'))
