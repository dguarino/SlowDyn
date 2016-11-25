
params = {
    'Modifiers.py.properties.b':[0.,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.070],
    'Modifiers.py.properties.a' : [9.,9.5,10,10.3,10.6,10.9,11.2,11.5,11.8,12.,12.2,12.5,12.8,13.1,13.4,14,14.5,15.],
    #'Modifiers.py.properties.a' : ,
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
