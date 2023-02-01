'''
플라스크 서버
- 문서 작성에 필요한 정보를 받아서 한글(hwp) 문서 생성
- 생성한 문서를 클라이언트에게 전달
    - hwp 및 pdf 파일 전송
'''

from flask import Flask 
   
def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    from server.views import main_views
    app.register_blueprint(main_views.bp)

    return app
