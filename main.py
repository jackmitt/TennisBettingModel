import data_manipulation as dm
import prediction_evaluation as pe
from helpers import match_prob

#dm.assemble_data()
#dm.pre_match_stats(path="./csv_data/6.0/")
#dm.train_test_split(path="./csv_data/6.0/")
#dm.predict(path = "./csv_data/6.0/", method = "neural_network")
#pe.simulateKellyBets(20000, kellyDiv = 1, pred_path='./csv_data/6.0/neural_network_predictions.csv')
#pe.simulateFixedBets(20000, pred_path='./csv_data/6.0/logistic_regression/predictions.csv')
#print (MC_game(0.6, 0.8, 0.84, 0.63))
print (match_prob(0.6544, 0.695, 0.874, 0.574, 0.651, 0.71, 0.909, 0.58, bestOf = 3))
