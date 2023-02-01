from dataclasses import dataclass
import hashlib
import time

def gen_doc_id() -> str:
    cur_time =  str(time.time())
    encoded_str =  cur_time.encode()
    hexdigest = hashlib.sha256(encoded_str).hexdigest()
    return hexdigest.rsplit(':', maxsplit=1)[-1].strip()

@dataclass
class OfficialDocumentTemplate:
    # 공문 상단 헤더
    receiver: str = ''  # 수신
    referrer: str = ''  # (경유)
    title: str = ''     # 문서 제목
    contents: str = ''  # 문서 내용 (본문)
    attach: str = ''    # 붙임 목록

    ### 공문 하단 - 결재자 정보 ###
    # 기안자
    member_name: str = ''       # 기안자 이름
    member_date: str = ''       # 기안자 결재 의뢰 일자
    member_sign: str = ''       # 기안자 서명 이미지 경로

    # 팀장
    leader_name: str = ''       # 팀장 이름
    leader_date: str = ''       # 팀장 결재 일자
    leader_sign: str = ''       # 팀장 서명 이미지 경로

    # 상속에 의해 결재자 추가 
    
    # 기관장
    director_name: str = ''     # 센터장 이름
    director_date: str = ''     # 센터 결재 일자
    director_sign: str = ''     # 센터 서명 이미지 경로
    
    # 공문 하단 - 협조자 정보
    co_workder1_name: str = ''     # 협조자1 이름
    co_workder2_date: str = ''     # 협조자1 결재일
    co_workder1_name: str = ''     # 협조자2 이름
    co_workder2_date: str = ''     # 협조자2 결재일

    doc_id: str = ''               # 문서번호
    effective_date: str = ''       # 문서 시행일 (센터장 결재일과 동일)


if __name__=='__main__':
    gen_doc_id()
    doc = OfficialDocumentTemplate()
    print(doc)