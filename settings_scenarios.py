import numpy as np

dummy_settings = {
    '0': {
        'log_amount' : [2, 4],
        'client_count' : [ 1, 2]
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

settings_1 = {
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

settings_2 = {
    '0': {
        'log_amount' : [int(x) for x in np.linspace(200, 2000, 10)],
        'client_count' : [int(x) for x in np.linspace(2, 40, 20)]
    },
    # '0': {
        # 'log_amount' : [200, 400, 600, 800, 1000, 1200],
        # 'client_count' : [2, 4, 6 ,8, 10, 12]
    # },
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
