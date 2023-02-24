import json
import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for
from server.forms import DocumentRequestForm
from doc_factory.template_data import DOC_TEMPLATE_CMSC_OFFICIAL
from doc_factory.factory import choose_factory, builder
from socket_client import SocketClient

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def home():
    data = {
        'title': request.args.get('title'),
        'content': request.args.get('content'),
    }
    print(f'title: {data["title"]}')
    print(f'content: {data["content"]}')

    return 'this is home'
    # return redirect(url_for('main.request_form'))


@bp.route('/gen_doc/')
def gen_doc():
    form = DocumentRequestForm()
    return render_template(
        'cmsc/gen_doc.html',
        form=form,
    )


@bp.route('/process_data/', methods=['GET', 'POST'])
def process_data():
    form = DocumentRequestForm()
    doc_info = DOC_TEMPLATE_CMSC_OFFICIAL
    if request.method == 'POST' and form.validate_on_submit():
        organization = request.form.get('organization')
        if organization is None:
            flash('기관 정보를 찾을 수 없습니다.\n시스템 관리자에게 문의하세요.')
            return redirect(url_for('main.gen_doc'))
        organization = organization.lower()

        doc_info['receiver']= request.form.get('receiver')
        doc_info['referrer'] = request.form.get('referrer')
        doc_info['title'] = request.form.get('title')
        doc_info['contents'] = request.form.get('contents')
        doc_info['attach'] = request.form.get('attach')

        factory = choose_factory(organization)
        if factory is None:
            flash(f'{organization}: 알수 없는 기관의 요청입니다.')
            return redirect(url_for('main.gen_doc'))
        # print(f'file_info: {file_info}')
        file_info = builder(factory, doc_info)
        
    return '데이터 프로세싱'

@bp.route('/process_data_remote_request/', methods=['POST'])
def process_data_remote_request():
    if request.is_json:
        doc_info = request.get_json()
    organization = doc_info.get('organization')
    factory = choose_factory(organization)
    if factory is None:
        print(f'{organization}: 알수 없는 기관의 요청입니다.')
        return 'Unknown organization'
    result = builder(factory, doc_info)
    status = 'success' if result['status'] else 'fail'
    print(f'hwp & pdf generation status: {status}')
    
    # 파일 생성에 성공했다면 리눅스 서버로 파일 전송
    if status == 'success':
        socket = SocketClient()
        socket.send_file(result['hwp_path'])
        socket.send_file(result['pdf_path'])
        
        
    return 'hwp/pdf 파일 생성'
