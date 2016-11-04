
params = {
    'run_time' : [5000],
    'Populations.py.n' : [1600],
   # 'Modifiers.py.cells.end' : [0.05,0.1,0.15],
   # 'Modifiers.py.properties.a' : [0.005,0.01,0.02],
    'Populations.py.cellparams.b': [0.02]#, 0.005],
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
