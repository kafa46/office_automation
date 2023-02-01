import hashlib
import os

from secret.secret_key import DATA_EXCHANGE_PASSWORD, CSRF_PASSWORD

# 프로젝트 홈 디렉토리
BASE_DIR = os.path.dirname(__file__)

# 데이터 교환을 위한 비밀키
REQUEST_SECRET = hashlib.sha256(DATA_EXCHANGE_PASSWORD.encode()).hexdigest()

# csrf 토큰 키
SECRET_KEY = hashlib.sha256(CSRF_PASSWORD.encode()).hexdigest()
