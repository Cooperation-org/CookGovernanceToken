from flask import Flask
from flask import render_template_string
from flask_menu import Menu, register_menu

app = Flask(__name__)
Menu(app=app)

def tmpl_show_menu():
    return render_template_string(
        """
        {%- for item in current_menu.children %}
            {% if item.active %}*{% endif %}{{ item.text }}
        {% endfor -%}
        """)

@app.route('/')
@register_menu(app, '.', 'Dashboard')
def dashboard():
    return tmpl_show_menu()

@app.route('/review')
@register_menu(app, '.review', 'Review', order=0)
def review():
    # generate what the updates would be since last time

    # push to a google sheet for $ and for cook

    # provide buttons to separately approve cook and cash
    return tmpl_show_menu()

@app.route('/review')
@register_menu(app, '.review', 'Review', order=0)
def approve_cook():

    # if approved, have button to register into pending totals
    # then also tag and push to historical the items counted in pending
    # and record the transaction in a log
    return tmpl_show_menu()

@app.route('/mint')
@register_menu(app, '.second', 'Second', order=1)
def second():
    return tmpl_show_menu()

if __name__ == '__main__':
    app.run(debug=True)

