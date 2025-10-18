import pytz
from datetime import datetime

# 한국시간대 설정
kst = pytz.timezone("Asia/Seoul")

# 오늘 날짜
today = datetime.now(kst).date()
