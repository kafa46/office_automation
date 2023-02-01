'''
Factory for generating documents.
한글문서 양식을 채워서 새로운 문서로 생성

Purpose:
    - 클라이언트 요청에 의해 새로운 문서를 생성/저장
    - 새 문서를 클라이언트에게 제공

Note:
    - MS Office, HWP와 같은 윈도우 전용 SW의 경우 윈도우 OS에서 동작해야 함
    - 윈도우 OS를 가상머신에 올릴 경우 네트워크 작업이 복잡해짐
    - 별도의 윈도우 서버 운영을 추천함

Written by Giseop Noh
Feb, 2023.
'''

from abc import ABC, abstractmethod
from doc_factory.template_data import OfficialDocumentTemplate
from datetime import datetime

class DocumentFactory(ABC):
    '''문서 생성 추상 클래스'''
    
    @abstractmethod
    def get_data(self, data: OfficialDocumentTemplate) -> OfficialDocumentTemplate:
        '''문서 생성에 필요한 추가 정보 생성
        '''
    
    @abstractmethod
    def read_doc(self, f_name: str) -> object:
        '''파일명을 받아서 파일 객체를 생성하여 리턴'''
    
    @abstractmethod
    def gen_doc(self, f_ogj: object) -> dict:
        '''파일 객체를 전달받아 새로운 파일을 생성
        Return: dict {
            'file_name': str # 파일 이름,
            'save_dir': str # 파일 저장 경로,
        }
        '''

class CMSCDocumentFactory(DocumentFactory):
    '''청원다문화지원센터(cmsc) 문서 생성'''
    
    def get_data(self, data: OfficialDocumentTemplate) -> OfficialDocumentTemplate:
        '''추가 정보 생성'''
        data.member_date = datetime.now().strftime('%y.%m.%d')
        
        return data

    def read_doc(self, f_name: str) -> object:
        return True
        
    def gen_doc(self, f_ogj: object) -> dict:
        return True

    def __str__(self) -> str:
        return 'cmsc object'

class PenielDocumentFactory(DocumentFactory):
    '''오송생명교회(peniel) 문서 생성'''
    
    def get_data(self, data: OfficialDocumentTemplate) -> OfficialDocumentTemplate:
        return True
    
    def read_doc(self, f_name: str) -> object:
        return True
        
    def gen_doc(self, f_ogj: object) -> dict:
        return True

    def __str__(self) -> str:
        return 'peniel object'


def choose_factory(fatcory_type: str) -> DocumentFactory:
    factories = {
        'cmsc': CMSCDocumentFactory(),
        'peniel': PenielDocumentFactory(),
    }
    
    if fatcory_type in factories:
        return factories[fatcory_type]
    
    print(f'{fatcory_type} >>> 알수 없는 기관의 문서 요청입니다.')
    return None


def builder(factory: DocumentFactory, doc_info: OfficialDocumentTemplate) -> str:
    '''Main function.'''
    
    doc_data = factory.get_data(doc_info)
    tempalte_doc = factory.read_doc()

    # return file path (saved location including file name)


if __name__=='__main__':
    doc_factory = choose_factory('cmsc')
    print(f'Factory type: {doc_factory}')