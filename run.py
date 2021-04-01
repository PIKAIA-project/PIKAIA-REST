from pikaia import app

# Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)

    # set FLASK_APP=run.py
    # flask run
