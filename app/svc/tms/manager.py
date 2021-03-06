"""
    service manager
"""
import argparse

# actions for app
actions = ['start', 'stop']

# registered apps
apps = ['crond', 'trade', 'quote', 'broker']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=actions)
    parser.add_argument('app', choices=apps)
    parser.add_argument('port', type=int)

    args = parser.parse_args()

    action, app, port = args.action, args.app, args.port

    if action == 'start':
        if app == 'crond':
            from . import crond
            crond.service.start(port)
        elif app == 'trade':
            from . import trade
            trade.service.start(port)
        elif app == 'quote':
            from . import quote
            quote.service.start(port)
        elif app == 'broker':
            from . import broker
            broker.service.start(port)
        else:
            pass
    elif action == 'stop':
        if app == 'trade':
            pass
        elif app == 'quote':
            pass
        else:
            pass
    else:
        pass
