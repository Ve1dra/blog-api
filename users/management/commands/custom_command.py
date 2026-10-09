import redis
from django.core.management.base import BaseCommand
from decouple import config
# # Connect to Redis
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.redis()

    def redis(self):
        redis_url = config("REDIS")
        r = redis.Redis.from_url(redis_url)
        # Send a ping request and check the response
        response = r.ping()
        print("Response:", response)