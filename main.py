import data_manipulation as dm
import prediction_evaluation as pe

#dm.assemble_data()
#dm.pre_match_stats(path="./csv_data/6.0/")
#dm.train_test_split(path="./csv_data/6.0/")
#dm.predict(path = "./csv_data/6.0/", method = "points_based")
pe.simulateKellyBets(20000, kellyDiv = 1, pred_path='./csv_data/6.0/points_based_predictions.csv')
#pe.simulateFixedBets(20000, pred_path='./csv_data/6.0/logistic_regression/predictions.csv')
