"""
    service manager
"""
import argparse

# actions for app
actions = ['start', 'stop']

# registered apps
apps = ['aam', 'aim', 'atm']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=actions)
    parser.add_argument('app', choices=apps)
    parser.add_argument('port', type=int)

    args = parser.parse_args()

    action, app, port = args.action, args.app, args.port

    if action == 'start':
        if app == 'aam':
            import app.aam;
            app.aam.service.start(port);
        elif app == 'aim':
            import app.aim
            app.aim.service.start(port)
        elif app == 'atm':
            import app.atm
            app.atm.service.start(port)
        else:
            pass
    elif action == 'stop':
        if app == 'aam':
            pass
        elif app == 'aim':
            pass
        elif app == 'atm':
            pass
        else:
            pass
    else:
        pass
