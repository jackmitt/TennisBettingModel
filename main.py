import data_manipulation as dm
import prediction_evaluation as pe

#dm.assemble_data()
dm.pre_match_stats()
dm.train_test_split()
dm.logistic_regression()
pe.simulateKellyBets(20000, kellyDiv = 1)
#pe.simulateFixedBets(20000)
