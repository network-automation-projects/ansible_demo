from flask import Flask

app = Flask(__name__)

#decorators

def make_bold(function):
    def wrapper():
        return "<b>" + function + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/username/<name>/1")  # this needs converter to string otherwise the /1 won't be part of the path correctly?
def greet(name):
    return f"Hello, {name}"

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye!"

if __name__ == '__main__':
    app.run(debug=True)  # this makes it restart automatically
                          #



# more common in real life:
# Use Jinja2 templates and put the HTML (and styling) there, or
#or
# use a helper function to style the text

# def styled(text: str, bold: bool = False, emphasis: bool = False, underlined: bool = False) -> str:
#     if bold:
#         text = f"<b>{text}</b>"
#     if emphasis:
#         text = f"<em>{text}</em>"
#     if underlined:
#         text = f"<u>{text}</u>"
#     return text

# @app.route("/bye")
# def bye():
#     return styled("Bye!", bold=True, emphasis=True, underlined=True)