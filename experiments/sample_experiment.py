experiment = {
    'parameters': [
        'x',
    ],
    'setup': """
    x = 1
    assert x == 1
    """,
    'experiment': """
    x += 1
    assert x == 2
    """,
    'analysis': """
    x += 1
    assert x == 3
    """,
}

# Build json file when this file is run
if __name__ == '__main__' and False:
    import json

    fname = __file__[:-3] + '.json'
    with open(fname, 'w') as f:
        json.dump(experiment, f, indent=4, sort_keys=True)
