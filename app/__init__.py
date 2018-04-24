from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from urllib.parse import urlparse
import click
import subprocess
import shlex
import os
import sys

from config import Config


def cmd_run(cmd: str, *args, **kwargs):
    """ Used to run a commandline program """
    completed_process = subprocess.run(shlex.split(cmd), *args, **kwargs)
    if completed_process.returncode != 0:
        sys.exit(completed_process.returncode)
    return completed_process


def project_path(path: str):
    root = os.environ.get('PROJECT_ROOT') or os.getcwd()
    return f'{root}/{path}'


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.logout_view = 'auth.logout'
bootstrap = Bootstrap()
toolbar = DebugToolbarExtension()


def create_app(config_class=Config):
    """ Flask factory to create an app """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    #: if testing recreate the database
    if app.config['TESTING']:
        uri = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
        if uri.path and os.path.exists(uri.path):
            os.unlink(uri.path)

        with app.app_context():
            db.create_all()

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
        cmd_run(
            f'python -m http.server {port}',
            cwd=project_path('/docs/build/html'))

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
            cmd_run('sphinx-apidoc -f -o source/ ..', cwd=f'{os.getcwd()}/docs')
        cmd_run('make coverage', cwd=project_path('/docs'))
        cmd_run('make html', cwd=project_path('/docs'))

    @app.cli.group(invoke_without_command=True)
    @click.pass_context
    def test(ctx):
        """
        Run all tox test
        """
        if ctx.invoked_subcommand is None:
            cmd_run('tox')

    @test.command()
    def lint():
        """
        Run autoformat and lint code (eyapf & flake8)
        """
        cmd_run('tox -e yapf,lint')

    return app


from app import routes, models  # noqa: ignore=E401
