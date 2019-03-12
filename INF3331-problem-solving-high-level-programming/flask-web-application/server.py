from flask import Flask, render_template, request, send_from_directory
import temperature_CO2_plotter as tc_plotter
import glob
import os

app = Flask(__name__)
app.config['DOC_FOLDER'] = 'doc/_build/html/'

docfiles = [os.path.basename(x) for x in glob.glob('doc/_build/html/*.html')]

@app.route("/", defaults={"filename": ''})
# @app.route("/")
@app.route("/<filename>")
def root(filename):
    # return "{}".format(docfiles)
    if filename in docfiles:
        # Hard to reference html files from folders outside templates/ folder
        # so I did it all hacky like this to reference sphinx doc files.
        # Still does not seem to play nice, but I couldnt make readthedocs work
        # (couldnt use my github username or something).
        return send_from_directory(
            app.config['DOC_FOLDER'],
            filename
        )
    return render_template("choose_dataset.html")

# @app.route("/docs", defaults={"filename": 'index.html'})
# @app.route("/docs/<path:filename>")
# def docs(filename):
#     # return "{}".format(app.config)
#     # return render_template("_build/html/index.html")

# @app.route("/temperature-plot/choos-month")
# def temp_choose_month():
#     return render_template("temp-choose-month.html")

@app.route("/choose-month")
def choose_month():
    months, years = tc_plotter.get_temperature_months_and_years()
    return render_template("choose-month.html", months=months)

def year_in_valid_range(year, years):
    if year == None: # if None default year is chosen, which is in valid range
        return True
    else:
        return (years[0] <= year <= years[-1])


def convert_to_type(convert, string_arg):
    """ If the argument is an empy string, convert to None, else convert string
    to type specified with the convert function.

    Args:
        arg (string): argument to convert
        convert (function): to convert to int, pass the int() function
    """
    if (string_arg == None):
        return None
    return None if string_arg == '' else convert(string_arg)

@app.route("/temperature-plot")
def temperature_plot():
    """ Uses parameters from the choose-month form to plot temperature data.
    """
    selected_month = request.args.get('selected_month')
    year_from = convert_to_type(int, request.args.get('year_from'))
    year_to   = convert_to_type(int, request.args.get('year_to'))
    y_min   = convert_to_type(float, request.args.get('y_min'))
    y_max   = convert_to_type(float, request.args.get('y_max'))

    months, years = tc_plotter.get_temperature_months_and_years()
    if (not (year_in_valid_range(year_from, years) and year_in_valid_range(year_to, years))):
        # error if year not in appropriate range
        return render_template("choose-month.html", months=months,
                               error="Selected year must be between {} and {}.".format(years[0], years[-1]))

    # Receive unique image url from the plotter.
    img_url = tc_plotter.plot_temperature(month=selected_month, year_from=year_from, year_to=year_to,\
                                          y_min=y_min, y_max=y_max)
    return render_template("temperature-plot.html", month=selected_month, months=months,
                               img_url=img_url, selected_month=selected_month)

@app.route("/CO2-plot")
def CO2_plot():
    """ Uses parameters from the choose-month form to plot CO2 data.
    """
    years = tc_plotter.get_CO2_years()
    year_from = convert_to_type(int, request.args.get('year_from'))
    year_to   = convert_to_type(int, request.args.get('year_to'))
    y_min   = convert_to_type(float, request.args.get('y_min'))
    y_max   = convert_to_type(float, request.args.get('y_max'))

    if (not (year_in_valid_range(year_from, years) and year_in_valid_range(year_to, years))):
        # error if year not in appropriate range
        return render_template("choose-range-CO2.html",
                               error="Selected year must be between {} and {}.".format(years[0], years[-1]))

    # Receive unique image url from the plotter.
    img_url = tc_plotter.plot_CO2(year_from=year_from, year_to=year_to,\
                                          y_min=y_min, y_max=y_max)
    return render_template("CO2-plot.html", img_url=img_url)

@app.route("/CO2-bar")
def CO2_bar():
    upper = convert_to_type(float, request.args.get('upper'))
    lower = convert_to_type(float, request.args.get('lower'))

    img_url = tc_plotter.bar_CO2(lower, upper)
    return render_template("CO2-bar.html", img_url=img_url)

if __name__ == "__main__":
    app.run(debug=True)

