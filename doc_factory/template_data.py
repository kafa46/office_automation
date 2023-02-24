import hashlib
import time


DOC_TEMPLATE_CMSC_OFFICIAL = {
    # 공문 상단 헤더
    'receiver': '',  # 수신
    'referrer': '',  # (경유)
    'title': '',     # 문서 제목
    'contents': '',  # 문서 내용 (본문)
    'attach': '',    # 붙임 목록

    ### 공문 하단 - 결재자 정보 ###
    # 기안자
    'member_name': '',       # 기안자 이름
    'member_date': '',       # 기안자 결재 의뢰 일자
    'member_sign': '',       # 기안자 서명 이미지 경로

    # 팀장
    'leader_name': '',       # 팀장 이름
    'leader_date': '',       # 팀장 결재 일자
    'leader_sign': '',       # 팀장 서명 이미지 경로

    # 상속에 의해 결재자 추가 
    
    # 기관장 
    'director_name': '',     # 센터장 이름
    'director_date': '',     # 센터 결재 일자
    'director_sign': '',     # 센터 서명 이미지 경로
    
    # 공문 하단 - 협조자 정보
    'co_worker1_name': '',     # 협조자1 이름
    'co_worker1_date': '',     # 협조자1 결재일
    'co_worker2_name': '',     # 협조자2 이름
    'co_worker2_date': '',     # 협조자2 결재일

    'doc_id': '',               # 문서번호
    'effective_date': '',       # 문서 시행일 (센터장 결재일과 동일)
    'is_public': '공개',           # 문서공개 여부 (공개 또는 비공개)
}


# 직원 이름과 이미지 파일명 맵핑
CMSC_NAME_IMG_FILE_MAPPER = {
    '노기섭': 'gs_noh.png',
    '김현진': 'hj_kim.png',
    '홍성주': 'sj_hong.png',
    '직인': 'stamp.png'
}

if __name__=='__main__':
    pass