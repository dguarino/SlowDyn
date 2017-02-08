{

    'DistanceDep': True,
    'run_time': 100000, # ms
    'dt': 0.1, # ms
    'nb_runs':5,
    'push_interval':1000, #ms
    'nb_push':50, #number of spikes
    'spike_times':[],
    'Injections' : {
    },


    'Populations' : {
        'ext' : {
            'n' : 1,
            'type': sim.SpikeSourcePoisson,
            'cellparams' : {
                'start':0.0,
                'rate':50.,
                'duration':100.0
            }
        },
        'audio' : {
            'n' : 10,
            'type': sim.SpikeSourceArray,
            'cellparams' : {}
        },
       'py' : {
            'n': 160, # units
            'type': sim.EIF_cond_alpha_isfa_ista,
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
                'cm'         : 0.200,
                'a'          : 0.001,#0.8e-3 Naud et al. 2008
                'b'          : 0.1 #0.03
            }
        },
        'inh' : {
            'n': {'ref':'py','ratio':0.25},
            'type': sim.EIF_cond_alpha_isfa_ista,
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
                'cm'         : 0.200,
                'a'          : 0.001,#uS
                'b'          : 0.015 #nA
            }
        }

    },

    'Projections' : {
        'ext_py' : {
            'source' : 'ext',
            'target' : 'py',
            'connector' : sim.FixedProbabilityConnector(.2),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
        'audio_py' : {
            'source' : 'audio',
            'target' : 'py',
            'connector' : sim.FixedProbabilityConnector(.2),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
 	'audio_inh' : {
            'source' : 'audio',
            'target' : 'inh',
            'connector' : sim.FixedProbabilityConnector(.2),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 60e-3,
            'receptor_type' : 'excitatory'
        },

        'py_py' : {
            'source' : 'py',
            'target' : 'py',
            'connector' : sim.FixedProbabilityConnector(.2, allow_self_connections=False, rng=sim.random.NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
        'py_inh' : {
            'source' : 'py',
            'target' : 'inh',
            'connector' : sim.FixedProbabilityConnector(.2, allow_self_connections=False, rng=sim.random.NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
        },
        'inh_py' : {
            'source' : 'inh',
            'target' : 'py',
            'connector' : sim.FixedProbabilityConnector(.2, allow_self_connections=False, rng=sim.random.NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 67e-3,
            'receptor_type' : 'inhibitory'
        },
        'inh_inh' : {
            'source' : 'inh',
            'target' : 'inh',
            'connector' : sim.FixedProbabilityConnector(.2, allow_self_connections=False, rng=sim.random.NumpyRNG(1235342134, parallel_safe=False)),
            'synapse_type' : sim.StaticSynapse,
            'weight' : 67e-3,
            'receptor_type' : 'inhibitory'
        }
    },

    'Recorders' : {
        'py' : {
            'spikes' : 'all',

            'gsyn_exc' : {
                'start' : 0,
                'end' : 20,
            },
	    'gsyn_inh' : {
                'start' :0,
                'end' : 20,
            },
            'v' : {
                'start' : 0,
                'end' : 20,
            }
        },
        'inh' : {
            'spikes' : 'all',
            'gsyn_inh' :{
                'start' : 0,
                'end' : 20,
            },
            'gsyn_exc' : {
                'start' :0,
                'end' : 20,
            },
            'v' : {
                'start' : 0,
                'end' : 20,
            }
        },
	'audio' : {
	    'spikes': 'all',
	}

    },

    'Modifiers' :{
        'py' : {
            'cells' : {
                'start' : 0,
                'end' : .1
            },
            'properties' : {
                'tau_w' : 150.,
                'cm' : 0.15,
                'tau_m' : 30.0, #
                'a' : 13., #Alain 0.02, #uS
                'b' : .02 #0.0
            }
	}        
    }

}
