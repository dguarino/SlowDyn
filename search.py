params = {
    'Populations.py.n' : [80, 100],
    'Populations.inh.n' : [20, 25],
    'Populations.py.cellparams.b': [0.1, 0.01, 0.001],
    #'Populations.inh.cellparams.b': [0.02, 0.002],
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
