from function_thread import FunctionThread


def multi_map(function, sequence, *sequence_1, **kwargs):
    """
    multi_map(function, sequence[, sequence, ...], threads=None) -> list

    Return a list of the results of applying the function to the items of
    the argument sequence(s) using multi-threading. If keyword argument 'threads'
    is given then only that many threads will be used at a time. Useful for
    functions that take time to return like a function that does http requests.
    If more than one sequence is given, the function is called with an
    argument list consisting of the corresponding item of each sequence,
    substituting None for missing values when not all
    sequences have the same length.  If the function is None, return a list of
    the items of the sequence (or a list of tuples if more than one sequence).
    """

    # Raise exceptions in case of wrong parameter values
    for i, seq in enumerate((sequence,) + sequence_1):
        try:
            iterator = iter(seq)
        except TypeError, e:
            raise TypeError('argument {0} to multi_map() must support iteration'.format(str(i+1)))

    if kwargs.get('threads'):
        if not isinstance(kwargs['threads'], int) or kwargs['threads'] <= 0:
            raise TypeError('keyword argument \'threads\' must be of type \'int\' and greater that \'0\'')

    if function is not None and not callable(function):
        raise TypeError('\'{0}\' object is not callable'.format(function.__class__.__name__))

    # Local methods
    def safe_list_get(l, idx, default):
        try:
            return l[idx]
        except IndexError:
            return default

    def chunks(l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    # Main logic
    if function is None and not sequence_1:
        return list(sequence)

    n = max(map(len, (sequence,) + sequence_1))

    args_tuples = [
        tuple([
            safe_list_get(seq, i, None) for seq in (sequence,) + sequence_1
        ]) for i in xrange(n)
    ]

    if function is None:
        return args_tuples

    max_threads = n
    if kwargs.get('threads'):
        max_threads = kwargs['threads']

    threads = list()
    for args_tuples_1 in list(chunks(args_tuples, max_threads)):
        threads_1 = [FunctionThread(function, *args) for args in args_tuples_1]
        for t in threads_1:
            t.start()
        for t in threads_1:
            t.join()
        threads.extend(threads_1)

    return [x.response for x in threads]

