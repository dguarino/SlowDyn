from pyNN.nest import *
from pyNN.utility import Timer

params = {

    'DistanceDep': True,
    'run_time': 5000, # ms
    'dt': 0.1, # ms
    'Injections' : {
    },

    'Populations' : {
        'ext' : {
            'n' : 1,
            'type': SpikeSourcePoisson,
            'cellparams' : {
                'start':0.0,
                'rate':50.,
                'duration':100.0
            }
        },
       'py' : {
            'n': 1600, # units
            'type': EIF_cond_alpha_isfa_ista,
            'cellparams': {
                'tau_m'      : 20.0,             # ms
                'tau_syn_E'  : 5.0,
                'tau_syn_I'  : 10.0,
                'tau_refrac' : 2.5,
                'v_rest'     : -60.0,
                'v_reset'    : -60.0,
                'v_thresh'   : -50.0,
                'delta_T'    : 2.5, #0.8 Naud et al.2008
                'tau_w'      : 600.0,
                'cm'         : 0.200,
                'a'          : 0.001,#0.8e-3 Naud et al. 2008
                'b'          : 0.03
            }
        },
        'inh' : {
            'n': {'ref':'py','ratio':0.25},
            'type': EIF_cond_alpha_isfa_ista,
            'cellparams': {
                'tau_m'      : 20.0,             # ms
                'tau_syn_E'  : 5.0,
                'tau_syn_I'  : 10.0,
                'tau_refrac' : 2.5,
                'v_rest'     : -60.0,
                'v_reset'    : -60.0,
                'v_thresh'   : -50.0,
                'delta_T'    : 2.5,
                'tau_w'      : 600.0,
                'cm'         : 0.200,#uS
                'a'          : 0.001,#uS
                'b'          : 0.015 #nA
            }
        }

    },

    'Projections' : {
        'ext_py' : {
            'source' : 'ext',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.02),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
        'py_py' : {
            'source' : 'py',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.02, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
        'py_inh' : {
            'source' : 'py',
            'target' : 'inh',
            'connector' : FixedProbabilityConnector(.02, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
        'inh_py' : {
            'source' : 'inh',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.02, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 67e-3,
            'receptor_type' : 'inhibitory'
        },
        'inh_inh' : {
            'source' : 'inh',
            'target' : 'inh',
            'connector' : FixedProbabilityConnector(.02, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 67e-3,
            'receptor_type' : 'inhibitory'
        }

    
    },


    'Recorders' : {
        'py' : {
            'spikes' :  'all',
            'gsyn_exc' : {
                'start' :200,
                'end' : 210,
            },
            'v' : {
                'start' :200,
                'end' : 210,
            }
        },
        'inh' : {
            'spikes' :  {
                'start' : 0,
                'end' : 1000,
            },
            #'gsyn_inh' :{
            #    'start' : 0,
            #    'end' : 10,
           # },
            'v' : {
                'start' : 0,
                'end' : 10,
            }
        }


    },

    'Modifiers' :{
        'py' : {
        'cells' : {
               'start' : 0,
               'end' : 0.1
            },
            'properties' : {
                'tau_w' : 150.,
                'cm' : 0.15,
                'tau_m' : 30.0, #
                'a' : 12., #Alain 0.02, #uS
                'b' : .03 #0.0
            }
        }
    }

}
