from cms import config


def extend(context = None):
    """
        extend context with default common context
    :param context:
    :return:
    """
    if context is None:
        return config.default_context

    return context.update(config.default_context)
