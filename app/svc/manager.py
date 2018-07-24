"""
    service manager
"""
import sys, argparse

# actions for app
actions = ['start', 'stop']

# registered apps
apps = ['aim', 'api', 'trade', 'quote']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=actions)
    parser.add_argument('app', choices=apps)
    parser.add_argument('port', type=int)

    args = parser.parse_args()

    action, app, port = args.action, args.app, args.port

    if action == 'start':
        if app == 'aim':
            import app.aim
            app.aim.service.start(port)
        elif app == 'api':
            import app.api
            app.api.service.start(port)
        elif app == 'trade':
            import app.trade
            app.trade.service.start(port)
        elif app == 'quote':
            import app.quote
            app.quote.service.start(port)
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