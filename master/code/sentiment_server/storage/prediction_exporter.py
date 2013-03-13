import numpy as np
base_id = []
base_uid = []

def set_base_from_dataset(dataset):
  global base_id, base_uid
  npconv = np.array(dataset, copy=True)
  base_id = npconv[:,0]
  base_uid = npconv[:,1]
  return base_id, base_uid

def get_prediction_set(y_predict):
  return map(list, zip(base_id, base_uid, y_predict))

def predictions_as_str(y_predict):
  predictions = get_prediction_set(y_predict)
  ex = ["\t".join(x) for x in predictions]
  return "\n".join(ex) + "\n"