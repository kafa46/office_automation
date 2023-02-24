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

from time import sleep
import win32com.client as win32
import win32con
from abc import ABC, abstractmethod
from datetime import datetime
from config import CMSC_OFFICIAL_DOCUMENT_PATH, BASE_DIR
from utils.hwp_utils import adjust_page_ending, adjust_text_heading_space, gen_unique_file_name, insert_img, insert_text, remove_end_charactor, save_as_pdf

import os
import hashlib
from pathlib import Path

class DocumentFactory(ABC):
    '''문서 생성 추상 클래스'''
    
    @abstractmethod
    def get_data(self, doc_info: dict) -> dict:
        '''문서 생성에 필요한 추가 정보 생성
        '''
    
    @abstractmethod
    def read_doc(self,) -> object:
        '''파일명을 받아서 파일 객체를 생성하여 리턴'''
    
    @abstractmethod
    def gen_doc(self, f_obj: object, doc_info: dict) -> dict:
        '''파일 객체를 전달받아 새로운 파일을 생성
        Return: dict {
            'file_name': str # 파일 이름,
            'save_dir': str # 파일 저장 경로,
        }
        '''
    

class CMSCDocumentFactory(DocumentFactory):
    '''청원다문화지원센터(cmsc) 문서 생성'''
    
    def __repr__(self) -> str:
        return "청원다문화지원센터(cmsc) 문서 factory"

    def get_data(self, doc_info: dict) -> dict:
        '''추가 정보 생성'''
        # 기안자의 날짜 생성
        doc_info['member_date'] = datetime.now().strftime('%y.%m.%d')
        
        return doc_info

    def read_doc(self, file_name) -> object:
        # 템플릿 hwp 읽어서 새이름으로 ./output/ 경로에 저장
        hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
        hwp.XHwpWindows.Item(0).Visible = False
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        hwp.Open(CMSC_OFFICIAL_DOCUMENT_PATH)

        if not file_name.endswith('.hwp'):
            file_name += '.hwp'
        new_file_path = f'{BASE_DIR}\\doc_factory\\output\\{file_name}.hwp'
        hwp.SaveAs(new_file_path) 

        return hwp
        
    def gen_doc_with_img(self, hwp: object, doc_info: dict) -> dict:
        '''서명 이미지를 넣는 코드 - deprecated'''
        field_str = hwp.GetFieldList() # 한글 문서의 필드 리스트 확인
        field_list = [x for x in field_str.split('\x02')]
        
        # 모든 필드 내용을 적절히 업데이트
        for field_name in field_list: 
            if field_name in doc_info.keys():
                field_data = doc_info.get(field_name)
                if field_data: # 입력할 데이터가 있으면 적절히 입력
                    if  field_name.endswith('sign'): # 이미지 입력할 경우
                        position =  field_name.split('_')[0] # 현재 필드의 직위
                        if position == 'member':
                            img_owner_name = doc_info[f'{position}_name'] 
                        else:
                            img_owner_name = doc_info[f'{position}_name']
                        hwp.MovePos(3)
                        insert_img(hwp, field_name=field_name, name=img_owner_name)
                    else: # 텍스트 데이터는 그대로 입력
                        # 붙임 목록의 추가 -> 2번째 줄부터 들여쓰기 + '끝.' 입력 삭제
                        if field_name == 'attach':
                            field_data = adjust_text_heading_space(field_data)
                            field_data = remove_end_charactor(field_data)
                        field_data = field_data.replace('\n', '\n\r')
                        hwp.MoveToField(field_name)
                        hwp.PutFieldText(f'{field_name}{{{{{0}}}}}', field_data)
                else: # 데이터가 없는 경우 -> 공백문자 처리
                    hwp.PutFieldText(f'{field_name}{{{{{0}}}}}', ' ')
        
        # 페이지 마무리
        adjust_page_ending(hwp) 
        
        # 저장 및 종료
        hwp.MovePos(2) # 문서 시작으로 이동
        hwp.Save() # 저장
        save_path =  hwp.XHwpDocuments.Item(0).FullName # 파일 경로 추출
        hwp.Quit() # 한글 종료

        return {
            'object': hwp,
            'file_path': save_path,
        }




class PenielDocumentFactory(DocumentFactory):
    def get_data(self, doc_info: dict) -> dict:
        return None
    
    def read_doc(self,) -> object:
        pass
    
    def gen_doc(self, f_obj: object, doc_info: dict) -> dict:
        pass


def choose_factory(fatcory_type: str) -> DocumentFactory:
    factories = {
        'cmsc': CMSCDocumentFactory(),
        'peniel': PenielDocumentFactory(),
    }
    
    if fatcory_type in factories:
        return factories[fatcory_type]
    
    return None


def builder(factory: DocumentFactory, doc_info: dict) -> str:
    '''Main function.'''
    doc_info = factory.get_data(doc_info)
    hwp = factory.read_doc()
    hwp.XHwpWindows.Item(0).Visible = False
    result = factory.gen_doc(hwp, doc_info)
    return result

    # return file path (saved location including file name)
