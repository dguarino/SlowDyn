
params = {
    'Modifiers.py.properties.b':[0.,0.01,0.02,0.03,0.04,0.05,0.06,0.070,0.08,0.09,1.],
    'Modifiers.py.properties.a' : [8.,9.,10.,11.,12.,13.,14.,15.,16.,17.],
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
