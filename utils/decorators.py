from functools import wraps

def input_error(cmd='', expected_args=None, optional_args=None):
    if expected_args is None:
        expected_args = []
    if optional_args is None:
        optional_args = []

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError) as e:
                user_args = args[0] if args else []
                min_args = len(expected_args)
                max_args = len(expected_args) + len(optional_args)
                usage = f'{cmd} ' + \
                        ' '.join(f'<{arg}>' for arg in expected_args) + ' ' + \
                        ' '.join(f'({arg})' for arg in optional_args)
                usage = usage.strip()
                optionals_line = (f"\nOptional arguments: {', '.join(optional_args)}"
                                  if optional_args else "")
                if len(user_args) < min_args:
                    return (f'The "{cmd}" command expects at least {min_args} argument(s): '
                            f"{', '.join(expected_args)}."
                            f"{optionals_line}\nUsage: {usage}")
                elif len(user_args) > max_args:
                    return (f'Too many arguments given for "{cmd}". '
                            f'Maximum allowed is {max_args}.\nUsage: {usage}')
                else:
                    return str(e)
            except Exception as e:
                return f"Error: {e}"
        return inner
    return decorator