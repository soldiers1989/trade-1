"""
    service manager
"""
import sys, argparse

# actions for app
actions = ['start', 'stop']

# registered apps
apps = ['trade', 'quote']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=actions)
    parser.add_argument('app', choices=apps)
    parser.add_argument('port', type=int)

    args = parser.parse_args()

    action, app, port = args.action, args.app, args.port

    if action == 'start':
        if app == 'trade':
            import app.trade
            app.trade.service.run()
        elif app == 'quote':
            import app.quote
            app.quote.service.run()
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
