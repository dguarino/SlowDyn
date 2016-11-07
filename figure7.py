from pyNN.nest import *
from pyNN.utility import Timer

params = {

    'DistanceDep': True,
    'run_time': 5000., # ms
    'dt': 0.1, # ms

    'Populations' : {

        'ext' : {
            'n' : 1,
            'type': SpikeSourcePoisson,
            'cellparams' : {
                'start':0.0,
                'rate':50.,
                'duration':50.0
            }
        },

        'extB' : {
            'n' : 1,
            'type' : SpikeSourcePoisson,
            'cellparams' : {
                'start':0.0,
                'rate':50.,
                'duration': 50.
            }
        },


       'py' : {
            'n': 1600, # units
            'type': EIF_cond_alpha_isfa_ista,
            'cellparams': {
                'tau_m'      : 20.0, # ms
                'tau_syn_E'  : 5.0, #
                'tau_syn_I'  : 10.0, #
                'tau_refrac' : 2.5, #D
                'v_rest'     : -60.0,#D
                'v_reset'    : -60.0,#D
                'v_thresh'   : -50.0,#D
                'delta_T'    : 2.5, #0.8 Naud et al.2008
                'tau_w'      : 600.0,#D
                'cm'         : 0.200,#nF D = Cm/cm2 * Surface
                'a'          : 0.001,#
                'b'          : .005 #
            }
            #'initial_values': {
            #    'v': -60.0#
            #}
        },

        'inh' : {
            'n': 400,
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
                'tau_w'      : 600.0,#ms
                'cm'         : 0.200,#uS
                'a'          : 0.001e3,#uS
                'b'          : 0.0 #nA
            }
        },

        'pyB' : {
            'n': 400,
            'type' :  EIF_cond_alpha_isfa_ista,
            'cellparams' : {
                'tau_m'      : 20.0,             # ms
                'tau_syn_E'  : 5.0, #needs to change as ge/gi changes
                'tau_syn_I'  : 10.0,
                'tau_refrac' : 2.5,
                'v_rest'     : -60.0,
                'v_reset'    : -60.0,
                'v_thresh'   : -50.0,
                'delta_T'    : 2.5,
                'tau_w'      : 600.0,
                'cm'         : 0.200,#nF
                'a'          : 0.001e3,#uS
                'b'          : .005 #nA
            }
        },

        'inhB' : {
            'n': 100,
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
                'tau_w'      : 600.0,#ms
                'cm'         : 0.200,#uS
                'a'          : 0.001e3,#uS
                'b'          : 0.0 #nA
            }
        },

    },

    'Projections' : {
        # stimuli
        'ext_py' : {
            'source' : 'ext',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.02),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'extB_pyB' : {
            'source' : 'extB',
            'target' : 'pyB',
            'connector' : FixedProbabilityConnector(.02),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        # model connectivity
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
        },


        'pyB_pyB' : {
            'source' : 'pyB',
            'target' : 'pyB',
            'connector' : FixedProbabilityConnector(.08, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'pyB_inhB' : {
            'source' : 'pyB',
            'target' : 'inhB',
            'connector' : FixedProbabilityConnector(.08, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'inhB_pyB' : {
            'source' : 'inhB',
            'target' : 'pyB',
            'connector' : FixedProbabilityConnector(.08, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 67e-3,
            'receptor_type' : 'inhibitory'
        },

        'inhB_inhB' : {
            'source' : 'inhB',
            'target' : 'inhB',
            'connector' : FixedProbabilityConnector(.08, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 67e-3,
            'receptor_type' : 'inhibitory'
        },

        # internal connectivity
        'py_pyB' : {
            'source' : 'py',
            'target' : 'pyB',
            'connector' : FixedProbabilityConnector(.01, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'pyB_py' : {
            'source' : 'pyB',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.01, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'py_inhB' : {
            'source' : 'py',
            'target' : 'inhB',
            'connector' : FixedProbabilityConnector(.01, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'pyB_inh' : {
            'source' : 'pyB',
            'target' : 'inh',
            'connector' : FixedProbabilityConnector(.01, allow_self_connections=False, rng=NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

    },


    'Recorders' : {
        'py' : {
            'spikes' :  'all'
        },
        'inh' : {
            'spikes' :  'all'
        },
        'pyB' : {
            'spikes' :  'all'
        },
        'inhB' : {
            'spikes' :  'all'
        },
    },

    'Modifiers' :{

        # LTS Subgroup - 10% of Layer B
        'pyB' : {
        'cells' : {
               'start' : 0,
               'end' : 20 #.05
            },
            'properties' : {
                'a' : 0.02e3, #uS
                'b' : 0.0
            }
        }
    }

}
