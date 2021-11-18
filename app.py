import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open(f'model/model.json', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        Price = flask.request.form['Price']
        LivingMeasure = flask.request.form['LivingMeasure']
        Quality = flask.request.form['Quality']
        CeilMeasure = flask.request.form['CeilMeasure']
        LivingMeasure15 = flask.request.form['LivingMeasure15']
        RoomBath = flask.request.form['RoomBath']
        Sight = flask.request.form['Sight']
        Basement = flask.request.form['Basement']
        RoomBed = flask.request.form['RoomBed']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[Price, LivingMeasure, Quality, CeilMeasure, LivingMeasure15, RoomBath, Sight, Basement, RoomBed]],
                                       columns=['Price', 'LivingMeasure', 'Quality', 'CeilMeasure', 'LivingMeasure15', 'RoomBath', 'Sight', 'Basement', 'RoomBed'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'Price':Price,
                                                     'LivingMeasure':LivingMeasure,
                                                     'Quality':Quality,
                                                     'CeilMeasure':CeilMeasure,
                                                     'LivingMeasure15':LivingMeasure15,
                                                     'RoomBath':RoomBath,
                                                     'Sight':Sight,
                                                     'Basement':Basement,
                                                     'RoomBed':RoomBed},
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()