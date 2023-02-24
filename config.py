import hashlib
import os
import ntpath

from secret.secret_key import DATA_EXCHANGE_PASSWORD, CSRF_PASSWORD

# 프로젝트 홈 디렉토리
BASE_DIR = os.path.dirname(__file__)

# 데이터 교환을 위한 비밀키
REQUEST_SECRET = hashlib.sha256(DATA_EXCHANGE_PASSWORD.encode()).hexdigest()

# csrf 토큰 키
SECRET_KEY = hashlib.sha256(CSRF_PASSWORD.encode()).hexdigest()

### 공문서 템플릿 위치 ###
# 청원다문화지원센터
cmsc = 'server\\docs\\cmsc\\templates\\template_cmsc.hwp'
CMSC_OFFICIAL_DOCUMENT_PATH = os.path.join(BASE_DIR, cmsc)

### CMSC 공문서 조작 설정 ###
# CMSC 공문서 한장에 들어갈 최대 라인 수
CMSC_MAX_LINES_IN_PAGE_FIRST = 26 # 기안문 첫페이지
CMSC_MAX_LINES_IN_PAGE_AFTER = 34 # 두번째 페이지부터

# 끝단 조정을 위해 이동해야 하는 줄 수 (끝단 -> 기관명 바로 윗 줄까지 이동)
CMSC_STEPS_TO_MOVE_PAGE_TRIM_POSITION = 4

# 결재 서명 이미지 경로
CMSC_IMG_DIR = 'C:\\Users\\kafa46\\workspace\\flask\\office_automation\\server\\static\\imgs\\cmsc'

# 출력파일 저장 경로
FILE_OUTPUT_DIR = os.path.join(BASE_DIR, 'doc_factory\output')