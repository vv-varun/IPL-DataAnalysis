from joblib import load
import pandas as pd;

def predict_match_result(testdata):
    testinput = testdata.copy()
    testdata.pop('runs_to_win')
    mymodel = load('ml_model.joblib')
    tdf = pd.DataFrame([testdata])
    test_results = mymodel.predict(tdf)
    if test_results[0] == "Won":
        result = "Win"
    else:
        result = "Loose"
    message = "With " + testinput["runs_to_win"] + " runs to win and "
    message = message + testinput["wickets_in_hand"] + " wickets in hand, you are most likely to " + result + " this game."
    return message