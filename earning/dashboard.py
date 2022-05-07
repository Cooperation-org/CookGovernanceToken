from flask import Flask
from flask import render_template_string
from flask_menu import Menu, register_menu

from earnings import generate_cook_updates, record_pending_cook
from sheets import push_to_sheet, pull_from_sheet, move_sheet_to_processed

app = Flask(__name__)
Menu(app=app)

def gen_menu_string():
    return """<ul>
  {%- for item in current_menu.children recursive -%}
  <li>
    <a href="{{ item.url}}">{{ item.text }}</a>
    {%- if item.children -%}
    <ul>
      {{ loop(item.children) }}
    </ul>
    {%- endif -%}
  </li>
  {%- endfor -%}
</ul>
        """

def tmpl_show_menu():
    return render_template_string(gen_menu_string())

def show_data_to_approve(url):
    page = tmpl_show_menu()
    page += render_template_string("View COOK to approve <a target='_new' href='{{ url }}'>{{ url }}</a>", url=url)
    page += render_template_string("<p/><a href='/dash/approve'><button>Approve and Post</button></a>")
    return page


# get the total pq tags paid on the done tasks

# comptroller pushes button for next step if looks reasonable:

# store in db as pending

# generate final token assignments, submit to multisig approval

# update db move from pending to accounted_for

# need tables for :  cook_pending, cook_issued 

@app.route('/')
@app.route('/dash', strict_slashes=False)
@register_menu(app, '.', 'Dashboard')
def dashboard():
    return tmpl_show_menu()


@app.route('/dash/review', strict_slashes=False)
@register_menu(app, '.review', 'Review', order=0)
def review():
    # generate what the updates would be since last time
    df = generate_cook_updates()

    # push to a google sheet for $ and for cook
    url = push_to_sheet(df)

    # provide buttons to separately approve cook and cash
    return show_data_to_approve(url)

@app.route('/dash/approve')
@register_menu(app, '.approve', 'Approve', order=0)
def approve_cook():

    df = pull_from_sheet()

    # this should be atomic
    try:
        record_pending_cook(df)

        move_sheet_to_processed()

        return tmpl_show_menu() + "<H2>COOK is Recorded!</h2>"
    except Exception as e:
        return tmpl_show_menu() + "<h2>Error has occurred :</h2>{}".format(str(e))

@app.route('/dash/mint', strict_slashes=False)
@register_menu(app, '.mint', 'Mint', order=1)
def second():
    return tmpl_show_menu()

if __name__ == '__main__':
    app.run(debug=True)

