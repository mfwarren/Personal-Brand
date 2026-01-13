# Fabric For Development

Fabric is a pretty awesome tool for deploying projects. But it turns out that it's also pretty awesome for lots of other stuff.

At PyCon 2012 there was a talk given by Ricardo Kirkner (which you can watch [here](http://pyvideo.org/video/677/using-fabric-to-standardize-the-development-proce)) that inspired me to play around with fabric in some new ways.

It's possible to use fabric as a wrapper around the standard django ./manage.py script, to help setting up virtualenvs and install packages. Using fabric to script around these things means that there are fewer tools that new developers will need to get set up and know how to use. Scripts that normally might have been loose bash files can now be collected, organized and documented.

I'm currently working on a large django project with 4 other developers who are new to python and django. Getting everyone's development environment working was a big pain since there were multiple platforms (Mac and Linux) and different configurations for base packages. If I had thought of this sooner I might have been able to create a reliable fabric script so that "easy_install fabric; fab init_project" got them from zero to running django app.

There's also several oneliners that I run fairly regularly which can be saved in fabfile.py and called much easier. For example:

```python
def clean():
    local('find . -name "*\.pyc" -exec rm -r {} \;')
```

Now `fab clean` will clear out any .pyc files in the project.

It's also possible to manage the virtualenv environment through fabric:

```python
VIRTUALENV = '.virtualenv/'

def setup_virtualenv():
    created = False
    virtual_env = os.environ.get('VIRTUAL_ENV', None)
    if virtual_env is None:
        if not os.path.exists(VIRTUALENV):
            _create_virtualenv()
            created = True
        virtual_env = VIRTUALENV
    env.virtualenv = os.path.abspath(virtual_env)
    _activate_virtualenv()
    return created

def _activate_virtualenv():
    activate_this = os.path.abspath("%s/bin/activate_this.py" % env.virtualenv)
    execfile(activate_this, dict(__file__=activate_this))

def _create_virtualenv(clear=False):
    if not os.path.exists(VIRTUALENV) or clear:
        args = '--no-site-packages --distribute --clear'
        local("%s /usr/local/bin/virtualenv %s %s" % (sys.executable, args, VIRTUALENV), capture=False)

def virtualenv_local(command, capture=True):
    prefix = ''
    virtual_env = env.get('virtualenv', None)
    if virtual_env:
        prefix = ". %s/bin/activate && " % virtual_env
    command = prefix + command
    return local(command, capture=capture)

def manage(command, *args):
    virtualenv_local("python manage.py {0} {1}".format(command, ' '.join(args)), capture=False,)

def runserver(*args):
    manage('runserver', *args)
```

These functions let you create the virtualenv and run commands in the virtualenv (without having manually activated it). virtualenv_local wraps the call to fabric's "local" function and sources the activate script before launching the command specified. The manage function provides a way to call django's manage.py script, and the runserver function gives a way to use fabric to launch the server (in the virtualenv). So now the fab command can be used to consolidate both virtualenv tools and manage.py script into one document-able fabfile.py with a consistent command-line interface.
