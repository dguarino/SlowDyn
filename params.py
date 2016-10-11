

p_c = .02
b = 0.1
rng = NumpyRNG(1235342134, parallel_safe=False)
g_e = 6e-3         # nS
g_i = 67e-3        # nS
g_ext = 6e-3
stim_dur = 50.0
p_c = .02
#scale_factor = round((py_n+inh_n) / (pyB_n+inhB_n))
inter_p_c = .01
v_init = -60.0


params = {

    'DistanceDep': True,
    'run_time': 1000, # ms
    'dt': 0.1, # ms

    'Populations' : {
        'ext' : {
            'n' : 1,
            'type': SpikeSourcePoisson,
            'cellparams' : {
                'start':0.0,
                'rate':50.,
                'duration':stim_dur
            }
        }
       'py' : {
            'n': 400, # units
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
                'cm'         : 0.200,
                'a'          : 0.001e3,
                'b'          : b
            }
        },
        'inh' : {
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
                'tau_w'      : 600.0,
                'cm'         : 0.200,
                'a'          : 0.001e3,
                'b'          : 0.0
            }
        }
    },

    'Projections' : {
        'ext_py' : {
            'source' : 'ext',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.02),
            'synapse_type' : StaticSynapse(weight=g_ext),
            'receptor_type' : 'excitatory'
        },
        'py_py' : {
            'source' : 'py',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(p_c, allow_self_connections=False, rng=rng),
            'synapse_type' : StaticSynapse(weight=g_e),
            'receptor_type' : 'excitatory'
        },
        'py_inh' : {
            'source' : 'py',
            'target' : 'inh',
            'connector' : FixedProbabilityConnector(p_c, allow_self_connections=False, rng=rng),
            'synapse_type' : StaticSynapse(weight=g_e),
            'receptor_type' : 'excitatory'
        },
        'inh_py' : {
            'source' : 'inh',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(p_c, allow_self_connections=False, rng=rng),
            'synapse_type' : StaticSynapse(weight=g_i),
            'receptor_type' : 'inhibitory'
        },
        'inh_inh' : {
            'source' : 'inh',
            'target' : 'inh',
            'connector' : FixedProbabilityConnector(p_c, allow_self_connections=False, rng=rng),
            'synapse_type' : StaticSynapse(weight=g_i),
            'receptor_type' : 'inhibitory'
        }
    },

    'Recorders' : {
        'py' : {
            'spikes' :  {
                'start' : 0,
                'end' : 10,
            },
            'v' : {
                'start' : 0,
                'end' : 10,
            }
        },
        'inh' : {
            'spikes' :  {
                'start' : 0,
                'end' : 10,
            },
            'v' : {
                'start' : 0,
                'end' : 10,
            }
        }
    },

    'Modifiers' :{
        'py' : {
            'start' : 0,
            'end' : .1
        }
    }

}
