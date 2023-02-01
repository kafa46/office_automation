from flask import Blueprint, request

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