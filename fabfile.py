#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'alex'
import os
from fabric.decorators import task
from fabric.api import run
from fabtools import require
from fabtools.python import virtualenv
from fabtools import supervisor
from fabric.contrib.files import exists
from fabric.operations import put
from cStringIO import StringIO



PROJECT_NAME = 'priceguru'
DOCUMENT_ROOT = os.getcwd()
RELEASE_PREFIX = ["release", 'debug'][__debug__]

SUPERVISORD_UWSGI = "_".join([PROJECT_NAME, 'uwsgi', RELEASE_PREFIX])
SUPERVISORD_CELERYD = "_".join([PROJECT_NAME, 'celeryd', RELEASE_PREFIX])


@task
def deps():
    require.deb.packages([
        "build-essential",
        'python-dev', 'gettext',
        'libpq-dev',
	'rabbitmq-server', 'redis-server',
        'python-virtualenv',
        'libxml2-dev', 'libxslt-dev',  # python lxml deps
        'libjpeg-dev', 'libfreetype6', 'libfreetype6-dev', 'zlib1g-dev',
        'libcurl4-gnutls-dev',
        'uwsgi', 'uwsgi-plugin-python', 'libpcre3', 'libpcre3-dev', # for uWsgi support
        'sendmail',
    ])
    print """
if your OS is Ubuntu you must make before install requirement
# ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
# ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
# ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
    """


@task
def requirements():
    require.python.virtualenv(os.path.join(DOCUMENT_ROOT, '.env'))
    with virtualenv(os.path.join(DOCUMENT_ROOT, '.env')):
        run('pip install distribute==0.6.35 -U')
        require.python.requirements(os.path.join(DOCUMENT_ROOT, "requirements.txt"))


@task
def uwsgi_add(user='alex'):
    kwargs = dict(
               command="uwsgi --ini {root}/conf/uwsgi.ini".format(root=DOCUMENT_ROOT),
               directory=DOCUMENT_ROOT,
               autorestart=True,
               stdout_logfile=os.path.join(DOCUMENT_ROOT, 'logs/uwsgi_out.log'),
               stderr_logfile=os.path.join(DOCUMENT_ROOT, 'logs/uwsgi_err.log'),
               user=user,
    )
    if not __debug__:
        kwargs['environment'] = "PYTHONOPTIMIZE=1"
    require.supervisor.process(SUPERVISORD_UWSGI, **kwargs)

@task
def uwsgi_stop():
    supervisor.stop_process(SUPERVISORD_UWSGI)


@task
def uwsgi_start():
    supervisor.start_process(SUPERVISORD_UWSGI)


@task
def celerid_add(user='alex'):
    celerid = dict(
               command="{0}/.env/bin/python manage.py celeryd -B".format(DOCUMENT_ROOT),
               directory=DOCUMENT_ROOT,
               autorestart=True,
               stdout_logfile=os.path.join(DOCUMENT_ROOT, 'logs/celeryd_out.log'),
               stderr_logfile=os.path.join(DOCUMENT_ROOT, 'logs/celeryd_err.log'),
               user=user,
    )
    if not __debug__:
        celerid['environment'] = "PYTHONOPTIMIZE=1"
    require.supervisor.process(SUPERVISORD_CELERYD, **celerid)

@task
def celeryd_stop():
    supervisor.stop_process(SUPERVISORD_CELERYD)

@task
def celeryd_start():
    supervisor.start_process(SUPERVISORD_CELERYD)

@task
def add_server(user='alex'):
    uwsgi_add(user)
    celerid_add(user)

@task
def start_server():
    uwsgi_start()
    celeryd_start()


@task
def stop_server():
    uwsgi_stop()
    celeryd_stop()

@task
def restart_server():
    stop_server()
    start_server()

@task
def patch_config(domain='priceguru.dev'):
	paths = dict(
		project_root=DOCUMENT_ROOT,
		conf_root=os.path.join(DOCUMENT_ROOT, "conf"),
		logs_root=os.path.join(DOCUMENT_ROOT, "logs"),
		domain=domain,
	)

	if not exists(paths['conf_root'], use_sudo=False):
		run('mkdir {conf_root}'.format(**paths))
	uwsgi_ini = open("uwsgi.ini").read()
	nginx_conf = open("nginx.conf").read()
	uwsgi_ini = StringIO(uwsgi_ini % paths)
	nginx_conf = StringIO(nginx_conf % paths)
	print put(uwsgi_ini, os.path.join(paths['conf_root'], 'uwsgi.ini'))
	print put(nginx_conf, os.path.join(paths['conf_root'], 'nginx.conf'))
