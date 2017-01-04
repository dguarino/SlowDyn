
params = {
    'Populations.re.cellparams.b':[0.01,0.05],
    'Populations.re.cellparams.a' : [20.,24.,32.],
    'Populations.tc.cellparams.b' : [0.02,0.03,0.04],
    'Populations.tc.cellparams.a' : [32.,34.],


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
