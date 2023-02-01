from flask import Blueprint, flash, redirect, render_template, request, url_for
from server.forms import DocumentRequestForm
from doc_factory.template_data import OfficialDocumentTemplate
from doc_factory.factory import choose_factory, builder

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
    doc_info = OfficialDocumentTemplate()
    if request.method == 'POST' and form.validate_on_submit():
        organization = request.form.get('organization')
        if organization is None:
            flash('기관 정보를 찾을 수 없습니다.\n시스템 관리자에게 문의하세요.')
            return redirect(url_for('main.gen_doc'))

        doc_info.receiver = request.form.get('receiver')
        doc_info.referrer = request.form.get('referrer')
        doc_info.title = request.form.get('title')
        doc_info.contents = request.form.get('contents')
        doc_info.attach = request.form.get('attach')

        factory = choose_factory(organization)
        if factory is None:
            flash(f'{organization}: 알수 없는 기관의 요청입니다.')
            return redirect(url_for('main.gen_doc'))
        file_info = builder(factory, doc_info)
        print(f'file_info: {file_info}')
        

    return '데이터 프로세싱'
