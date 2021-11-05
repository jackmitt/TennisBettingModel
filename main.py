import data_manipulation as dm
import prediction_evaluation as pe

#dm.assemble_data()
#dm.pre_match_stats()
#dm.train_test_split()
#dm.logistic_regression(path = "./csv_data/3.0/")
pe.simulateKellyBets(20000, kellyDiv = 1, pred_path='./csv_data/3.0/predictions.csv')
#pe.simulateFixedBets(20000)
