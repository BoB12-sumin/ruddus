from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>페이지 제목</title>
        <meta charset="UTF-8">
        <!-- 여기에 다른 메타 태그, CSS 파일 링크, 스크립트 등을 추가할 수 있습니다 -->
    </head>
    <body>
        <h1>헤딩111</h1>
        <h2>헤딩23</h2>
    </body>
    </html>
"""


@app.route("/user/<name>")
def username(name):
    return f"사용자 페이지, {name}"


@app.route("/user/<int:age>")
def userage(age):
    return f"사용자 페이지, {age}"


@app.route("/user/<float:weight>")
def userweight(weight):
    return f"사용자 페이지, {weight}"


@app.route("/user/<name>/<int:age>/<float:weight>")
def userinfo(name, age, weight):
    return f"사용자 info, {name}, {age}, {weight}"


if __name__ == "__main__":
    app.run(debug=True)
