
params = {
    'Populations.tc.cellparams.b':[-0.04,-0.03,-0.02,-0.01,0.,0.01,0.02,0.03,0.04,0.05,0.06],
    'Populations.tc.cellparams.a' : [20.,22.,24.,26.,28.,30.,32.,34.,36.,38.,40.],
    #'Populations.py.cellparams.b': [.1, .09, .08, .07, .06, .06, .05, .04, .04, .03, .02, .01],
    #'Populations.tc.cellparams.b': [.0, .00001, .0001, .001, .01],

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
