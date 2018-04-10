from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
import click
import subprocess
import shlex
import os

from config import Config


def run(cmd: str, *args, **kwargs):
    return subprocess.run(shlex.split(cmd), *args, **kwargs)


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.logout_view = 'auth.logout'
bootstrap = Bootstrap()
toolbar = DebugToolbarExtension()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    toolbar.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.rest import bp as rest_bp
    app.register_blueprint(rest_bp)

    @app.cli.group(invoke_without_command=True)
    @click.option(
        '--host',
        '-h',
        default='0.0.0.0',
        help='IP of interface to use for serving documentation')
    @click.option(
        '--port',
        '-p',
        default=5000,
        help='port to use for serving documentation')
    @click.option(
        '--apidoc/--no-apidoc',
        default=False,
        help='Whether to run sphinx-apidoc')
    @click.pass_context
    def docs(ctx, host, port, apidoc):
        """
        Generate docs and serve them
        """
        if ctx.invoked_subcommand is None:
            ctx.invoke(build, apidoc=apidoc)
            ctx.invoke(serve, host=host, port=port)

    @docs.command()
    @click.option(
        '--host', '-h', default='0.0.0.0', help='IP of interface to use')
    @click.option('--port', '-p', default=5000, help='port to use')
    def serve(host, port):
        """
        serve the documentation
        """
        click.echo(f'Serving HTML Documentation on {host}:{port}')
        click.echo('')
        run(f'python -m http.server {port}',
            cwd=f'{os.getcwd()}/docs/build/html')

    @docs.command()
    @click.option(
        '--apidoc/--no-apidoc',
        default=False,
        help='Whether to run sphinx-apidoc')
    def build(apidoc: bool):
        """
        build the documentation
        """
        click.echo('Making Sphinx HTML Documentation')
        click.echo('')
        if apidoc:
            run('sphinx-apidoc -f -o source/ ..', cwd=f'{os.getcwd()}/docs')
        run('make html', cwd=f'{os.getcwd()}/docs')

    @app.cli.command()
    def test():
        """
        Run tox
        """
        run('tox')

    return app


from app import routes, models  # noqa: ignore=E401
