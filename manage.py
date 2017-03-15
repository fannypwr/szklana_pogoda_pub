import os
from app import create_app, db
from app.models import User, Place, Temperature
from flask_script import Manager, Shell, Server

app = create_app(os.environ.get('SZCONFIG') or 'default')
manager = Manager(app)
server = Server(host="0.0.0.0", port=9000)

manager.add_command('runserver', server)


def make_shell_context():
    return dict(app=app, db=db, User=User, Place=Place, Temperature=Temperature)

manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
