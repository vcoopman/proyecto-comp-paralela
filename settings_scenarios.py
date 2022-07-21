import numpy as np

settings = {
    '0': {
        'log_amount' : [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
        'client_count' : [ 5, 10, 15, 20, 25, 30 ]
    },
    '1': {
        'log_amount' : [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
        'client_count' : [ 5, 10, 15, 20, 25, 30 ]
    },
    '2': {
        'log_amount' : [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
        'client_count' : [ 1, 2, 3, 4, 5 ],
        'rate': [ 1, 2, 5 ]
    }
}


dummy_settings = {
    '0': {
        'log_amount' : [1, 2, 3],
        'client_count' : [ 1, 2, 3]
    },
    '1': {
        'log_amount' : [1, 2, 3],
        'client_count' : [ 1, 2, 3]
    },
    '2': {
        'log_amount' : [1, 2, 3],
        'client_count' : [ 1, 2, 3],
        'rate': [ 1, 2, 3 ]
    }
}

dummy_settings_2 = {
    '0': {
        'log_amount' : [int(x) for x in np.linspace(10, 100, 10)],
        'client_count' : [int(x) for x in np.linspace(3, 9, 7)]
    },
    '1': {
        'log_amount' : [1, 2, 3],
        'client_count' : [ 1, 2, 3]
    },
    '2': {
        'log_amount' : [1, 2, 3],
        'client_count' : [ 1, 2, 3],
        'rate': [ 1, 2, 3 ]
    }
}
