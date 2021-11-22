import data_manipulation as dm
import prediction_evaluation as pe
from helpers import MCMC_game

#dm.assemble_data()
#dm.pre_match_stats(path="./csv_data/6.0/")
#dm.train_test_split(path="./csv_data/6.0/")
#dm.predict(path = "./csv_data/6.0/", method = "neural_network")
#pe.simulateKellyBets(20000, kellyDiv = 1, pred_path='./csv_data/6.0/neural_network_predictions.csv')
#pe.simulateFixedBets(20000, pred_path='./csv_data/6.0/logistic_regression/predictions.csv')
for l in range(100):
    print(MCMC_game(0.6, 0.8, 0.84, 0.63, 10000))
