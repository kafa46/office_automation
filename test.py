import win32com.client as win32
from doc_factory import factory
from doc_factory.template_data import DOC_TEMPLATE_CMSC_OFFICIAL
from config import CMSC_OFFICIAL_DOCUMENT_PATH

if __name__=='__main__':
    fac = factory.choose_factory('cmsc')
    doc_info = {
        'receiver':'청주대학교(소프트웨어)', 
        'referrer': '교무처장', 
        'title': '청원다문화가족지원센터 잔액확인증 제출',
        'contents': '''1. 관련근거
   가. 청주대 학칙(22.01.22) 제1장 교무행정
   나. 지방기관 운영에 대한 조례 충북-001(2015.06.24) 제 17조 3항

2. 위 관련근거에 따라 청원다문화가족지원센터는 다문화가족의 가족관계 향상을 도모하고, 지역사회 내에서 다문화가족에 대한 긍정적인 인식을 제고하며 사회통합을 지원하는 사업들을 운영하고 있습니다.

3. 법인 변경으로 인한 청원다문화가족지원센터의 잔액확인증을 청주대학교 산학협력단에 제출합니다.''',
        'attach': '''운영결과 보고서 1부.
청원다문화지원센터 사업자 등록증 1부.     끝.         ''',
        'member_name': '노기섭', 
        'member_date': '', 
        'member_sign': 'True',
        'leader_name': '홍성주', 
        'leader_date': '', 
        'leader_sign': 'True',
        'director_name': '김현진', 
        'director_date': '', 
        'director_sign': 'True',
        'co_worker1_name': '임동균', 
        'co_worker1_date': '',
        'co_worker2_name': '김헌일', 
        'co_worker2_date': '',
        'doc_id': '0001', 
        'effective_date': '',
        'is_public': '공개'
    }
    doc = factory.builder(fac, doc_info)
