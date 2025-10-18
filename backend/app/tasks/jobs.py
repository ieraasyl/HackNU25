from taskiq import TaskiqScheduler
from taskiq_redis import RedisBroker
from app.core.config import REDIS_URL

broker = RedisBroker(REDIS_URL)
scheduler = TaskiqScheduler(broker=broker)

@broker.task
async def process_candidate(candidate_id: str):
    print(f"Processing candidate {candidate_id}")
