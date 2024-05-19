'''
Author: Junyi_Li ljyduke@gmail.com
Date: 2024-05-15 20:44:04
LastEditors: Junyi_Li ljyduke@gmail.com
LastEditTime: 2024-05-15 20:44:34
FilePath: /Mayfif/app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 简单的HTML表单
HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Echo Service</title>
</head>
<body>
    <h2>Enter something to echo:</h2>
    <form method="post">
        <input type="text" name="echo_text" placeholder="Type something...">
        <input type="submit" value="Submit">
    </form>
    {% if echo_text %}
        <h3>You said: {{ echo_text }}</h3>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    echo_text = None
    if request.method == 'POST':
        echo_text = request.form['echo_text']
    return render_template_string(HTML_FORM, echo_text=echo_text)

if __name__ == '__main__':
    app.run(debug=True)