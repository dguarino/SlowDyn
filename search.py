
params = {
    'run_time' : [5000],
    'Populations.py.n' : [1600],
    #'Modifiers.py.cells.end' : [0.12,0.13,0.14],
   # 'Modifiers.py.properties.a' : [0.01, 0.03],
    'Populations.py.cellparams.b': [0.07,0.06,0.05,0.04,0.03,0.02,0.01, 0.005,0.001],
    'Populations.py.cellparams.a':[0.003,0.002,0.001,0.0005,0.0001]

}


# We want to be able, in run_parameter_search.py, to iterate over
# the parameters to be replaced in the full params.py file:
#[
#   {
#       'Populations.py.n' : 800,
#       'Populations.py.cellparams.b': 0.1,
#       'Populations.inh.cellparams.b': 0.02,
#   },
#   {
#       'Populations.py.n' : 800,
#       'Populations.py.cellparams.b': 0.1,
#       'Populations.inh.cellparams.b': 0.002,
#   },
#
# ...
#]
