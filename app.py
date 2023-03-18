from flask import Flask, render_template, request, redirect
import os
import signal

app = Flask(__name__)

file = 'data/text.txt'


def read():
    with open(file) as f:
        return f.readlines()


def write(content):
    with open(file, 'a') as f:
        f.write(content+'\n')


def rewrite(content):
    with open(file, 'w+') as f:
        f.writelines(content)


@app.route('/add', methods=["POST"])
def add():
    print(request.form)
    content = request.form.get("input")
    if content:
        write(content)
    return redirect('/')


@app.route('/')
def home():
    content = read()
    return render_template('index.html', content=content)


@app.route('/kill')
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return redirect('/')


@app.route('/delete/<row>')
def delete(row):
    print(row)
    print(type(row))
    content = read()
    print(content)
    content.remove(row+'\n')
    rewrite(content)
    return redirect('/')


if __name__ == "__main__":
    with open(file, 'a'):
        pass
    app.run(debug=True, host="0.0.0.0", port="5000")
