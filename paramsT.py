from pyNN.nest import *
from pyNN.utility import Timer

params = {

    'DistanceDep': True,
    'run_time': 10000, # ms
    'nb_runs' : 8,
    'dt': 0.1, # ms

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
       
        'tc' : {
            'n': 100,
            'type' :  EIF_cond_alpha_isfa_ista,
            'cellparams' : {
                'tau_m'      : 30.0,             # ms
                'tau_syn_E'  : 5.0, #needs to change as ge/gi changes
                'tau_syn_I'  : 10.0,
                'tau_refrac' : 2.5,
                'v_rest'     : -60.0,
                'v_reset'    : -60.0,
                'v_thresh'   : -50.0,
                'delta_T'    : 2.5,
                'tau_w'      : 150.0,
                'cm'         : 0.15,#nF
                'a'          : 13.,#uS
                'b'          : 0.0 #nA
            }

        },
        're' : {
            'n': 100,
            'type' :  EIF_cond_alpha_isfa_ista,
            'cellparams' : {
                'tau_m'      : 20.0,             # ms
                'tau_syn_E'  : 5.0,
                'tau_syn_I'  : 10.0,
                'tau_refrac' : 2.5,
                'v_rest'     : -60.0,
                'v_reset'    : -60.0,
                'v_thresh'   : -50.0,
                'delta_T'    : 2.5,
                'tau_w'      : 150.0,
                'cm'         : 0.15,#nF
                'a'          : 30.,#uS
                'b'          : 0.01 #nA
            }
        }


    },

    'Projections' : {
        'ext_tc' : {
            'source' : 'ext',
            'target' : 'tc',
            'connector' : FixedProbabilityConnector(.02),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },

        'tc_re' : {
            'source' : 'tc',
            'target' : 're',
            'connector' : FixedProbabilityConnector(.02, allow_self_connections=False),
            'synapse_type' : StaticSynapse,
            'weight' : 30e-3,
            'receptor_type' : 'excitatory'
        },

        're_tc' : {
            'source' : 're',
            'target' : 'tc',
            'connector' : FixedProbabilityConnector(.08, allow_self_connections=False),
            'synapse_type' : StaticSynapse,
            'weight' : 40e-3, #30e-3,
            'receptor_type' : 'inhibitory'
        },

        're_re' : {
            'source' : 're',
            'target' : 're',
            'connector' : FixedProbabilityConnector(.08, allow_self_connections=False),
            'synapse_type' : StaticSynapse,
            'weight' : 30e-3,
            'receptor_type' : 'inhibitory'
        },


    },


    'Recorders' : {


        'tc' : {
            'spikes' :  {
                'start' : 0,
                'end' : 100,
            },
            'gsyn_exc' :{
                'start' : 0,
                'end' : 10,
            },
            'v' : {
                'start' : 0,
                'end' : 10,
            }
        },
        're' : {
            'spikes' :  {
                'start' : 0,
                'end' : 100,
            },
            'gsyn_exc' :{
                'start' : 0,
                'end' : 10,
            },
            'v' : {
                'start' : 0,
                'end' : 10,
            }
        }

    },

    'Modifiers': {
    
    },

    'Injections': {
    },

}
