import hashlib
import win32con
import os
import re
from time import sleep
from datetime import datetime
from config import CMSC_MAX_LINES_IN_PAGE_FIRST
from config import CMSC_MAX_LINES_IN_PAGE_AFTER
from config import CMSC_STEPS_TO_MOVE_PAGE_TRIM_POSITION
from config import CMSC_IMG_DIR
from doc_factory.template_data import CMSC_NAME_IMG_FILE_MAPPER

def gen_unique_file_name():
    temp_str = str(datetime.now())
    return hashlib.sha256(temp_str.encode()).hexdigest()


def adjust_page_ending(hwp:object) -> object:
    '''공문 하단부에 여백이 있을 경우 하단 정보를 마지막으로 이동'''
    
    hwp.MovePos(3) # 문서의 끝으로 캐럿 이동
    page_num = hwp.KeyIndicator()[3] # 페이지
    line_num = hwp.KeyIndicator()[5] # 줄

    print(f'page: {page_num}, lines: {line_num}')
    
    # 만약 끝단 여분이 있다면 결제정보 블록을 끝단에 맞춤
    if page_num == 1:
        extra_lines = CMSC_MAX_LINES_IN_PAGE_FIRST - line_num
    else:
        extra_lines = CMSC_MAX_LINES_IN_PAGE_AFTER - line_num
    
    # print(f'current line number: {line_num}')
    # print(f'extra lines: {extra_lines}')

    # 여유 라인 수 만큼 엔터를 치기 위한 위치로 이동(CMSC의 경우 4줄)
    hwp.HAction.Run("MoveTopLevelEnd")  # 문서 마지막으로
    hwp.HAction.Run("MoveLineBegin")    # 현재 줄 처음으로
    for _ in range(CMSC_STEPS_TO_MOVE_PAGE_TRIM_POSITION):
        hwp.HAction.Run("MoveUp"); # 한 줄 위로 이동
    
    # 여유 라인 수 만큼 엔터키 
    for idx, _ in enumerate(range(extra_lines)):
        hwp.Run("BreakLine")
    
    return hwp


def insert_text(hwp:object, text):
    hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HParameterSet.HInsertText.Text = text
    hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)


def adjust_text_heading_space(text):
    text_list = text.splitlines()
    text_new = ''
    if len(text_list) > 1:
        for idx, text in enumerate(text_list):
            if idx == 0:
                text_new += text
                continue
            text_new += '\n      ' + text
        return text_new
    else:
        return text


def remove_end_charactor(text):
    text = text.strip()
    
    replace_dic = { # 치환할 단어 정의
        '끝.': '',
        '끝': '',
    }
    replace_dic = dict((re.escape(k), v) for k, v in replace_dic.items()) 
    pattern = re.compile("|".join(replace_dic.keys()))
    text_new = pattern.sub(lambda m: replace_dic[re.escape(m.group(0))], text)
    text_new = text_new.strip()

    return text_new


def insert_img(hwp:object, field_name: str, name: str) -> None:
    # 이미지 파일 경로 생성
    img_dir = os.path.join(CMSC_IMG_DIR, CMSC_NAME_IMG_FILE_MAPPER[name])
    
    # 해당 필드로 이동
    hwp.MoveToField(field_name)
    
    # 이미지 넣기
    hwp.InsertPicture(img_dir, Embedded=True, sizeoption=2)
    hwp.FindCtrl()  # 커서에서 인접한 개체 선택(양쪽에 있으면 우측개체 우선선택)
    hwp.HAction.GetDefault("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)  # 액션 초기화
    hwp.HParameterSet.HShapeObject.TextWrap = hwp.TextWrapType("BehindText")  # 글 뒤로 배치
    hwp.HParameterSet.HShapeObject.TreatAsChar = 0  # 글자처럼 취급 해제
    
    # result = hwp.HAction.Execute("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)  # 실행    
    # hwp.HAction.GetDefault("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)  # 액션 초기화
    # # 일반글자처럼 취급 해제
    # hwp.HAction.GetDefault("ShapeObjTreatAsChar", hwp.HParameterSet.HShapeObject.HSet)
    # hwp.HParameterSet.HShapeObject.TreatAsChar = 0
    # # 텍스트 위로 겹치기 설정
    # hwp.HAction.Execute("ShapeObjTreatAsChar", hwp.HParameterSet.HShapeObject.HSet)
    # hwp.HAction.Run("ShapeObjBringInFrontOfText")


def move_to_table(hwp:object, nth_table: int) -> bool:
    code = hwp.HeadCtrl
    paramSet = None
    list_ = 0
    para_ = 0
    pos = 0
    counter = 1
    while (code and code != hwp.LastCtrl):
        strID = code.CtrlID
        if strID=="tbl" and counter==nth_table:
            paramSet = code.GetAnchorPos(0)
            list_ = paramSet.Item("List")
            para_ = paramSet.Item("Para")
            pos = paramSet.Item("Pos")
            hwp.SetPos(list_, para_, pos)
            return True
        code = code.Next
        counter += 1
    return False
    
def save_as_pdf(hwp:object, file_name: str = None) -> None:
    if file_name:
        doc = hwp.XHwpDocuments.Item(0)
        file_path = hwp.XHwpDocuments.Item(0).FullName  # 경로 포함한 파일명
        print(f'Current file path: {file_path}')
        file_name = file_path.replace('.hwp', '.pdf')
        print(f'Target file path: {file_name}')
    
    
        # FileName 속성 에러 해결 
        #   -> https://martinii.fun/342 -> FileName --> filename
        hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)
        hwp.HParameterSet.HFileOpenSave.filename = file_name
        hwp.HParameterSet.HFileOpenSave.Format = 'PDF'
        hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)
        return file_name
    else:
        print('파일이 없어서 pdf 변환할 수 없습니다.')
        return None

