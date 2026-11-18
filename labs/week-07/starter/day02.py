"""Lab 2: validate a closed scalar schema before returning clean arguments."""
def validate(arguments, schema):
    if not isinstance(arguments, dict) or schema.get('additionalProperties') is not False:
        raise ValueError('closed object required')
    # TODO: enforce required/known keys, exact scalar types, length and ranges.
    return dict(arguments)
