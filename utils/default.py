import traceback

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(
        type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"

