import redis
import json
import traceback
from flask import current_app

# 레디스 연결 설정
def get_redis_connection():
    try:
        # 레디스 연결 정보
        redis_host = 'redis-10306.c340.ap-northeast-2-1.ec2.redns.redis-cloud.com'
        redis_port = 10306
        redis_username = "default"
        redis_password = "Tc01APaDSz7EZYoyKso9dMj1wfUIF9Uu"
        
        # 레디스 클라이언트 생성
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            username=redis_username,
            password=redis_password,
            decode_responses=True,
        )
        
        # 연결 테스트
        ping_result = r.ping()
        return r
    except Exception as e:
        print(f"[Redis 연결 오류] {str(e)}")
        traceback.print_exc()
        return None
