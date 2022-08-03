import utils

def eval_func(payload):
    """
            Eval if conditions true or false.

            ---
            Input:
                payload: dict # Request payload dict format.

            ----
            Return:
                trueConditions: integer[] # numeration of true conditions.
                context: dict # The resulting context after evaluating conditions.
    """

    payload['log']['Text'] = utils.clean_log_text(payload['log']['Text'])
    context = payload['context'] # context to use for this checks. This will be updated after every true condition check.

    true_conditions = [] # stores numerations of true conditions.

    for cond in payload['conditions']:
        try:
            if cond['type'] == 'Standard':
                result = utils.eval_condition_text(cond['text'], payload['log'], context)
                if result[0]:
                    true_conditions.append(cond['numeration'])
                    context = result[1]

            elif cond['type'] == 'Timed':
                # Check text
                result1 = utils.eval_condition_text(cond['text'], payload['log'], context)

                # Check time
                result2 = (payload['logProcessingTime'] - payload['stateTime'] <= cond['timeRange'])

                if result1[0] and result2:
                    true_conditions.append(cond['numeration'])
                    context = result1[1]

            elif cond['type'] == 'Order':
                all_true_conditions = payload['trueConditions'] + true_conditions
                if len(all_true_conditions) >= len(cond['order']):
                    # Check if order match
                    main_str = ''.join([str(x) for x in all_true_conditions])
                    sub_str = ''.join([str(x) for x in cond['order']])
                    if sub_str in main_str:
                        true_conditions.append(cond['numeration'])

        except Exception as e:
            print(e)
            return { 'error': str(e), 'condition': cond }

    return { 'trueConditions': true_conditions, 'context': context }
