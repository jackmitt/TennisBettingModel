import data_manipulation as dm
import prediction_evaluation as pe

#dm.assemble_data()
dm.pre_match_stats(path="./csv_data/3.4.2/")
dm.train_test_split(path="./csv_data/3.4.2/")
dm.logistic_regression(path = "./csv_data/3.4.2/")
pe.simulateKellyBets(20000, kellyDiv = 1, pred_path='./csv_data/3.4.2/predictions.csv')
#pe.simulateFixedBets(20000)
