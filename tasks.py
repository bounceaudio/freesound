import os

from invoke import task

CHECK_DIRS = "src/freesound"
DIRNAME = os.path.dirname(__file__)
MYPY_CONFIG = os.path.join(DIRNAME, "mypy.ini")


@task
def linters(ctx):
    cmd = "ruff check"
    print(cmd)
    ctx.run(cmd)


@task
def code_style(ctx):
    cmd = "ruff format --check"
    print(cmd)
    ctx.run(cmd)


@task
def mypy(ctx):
    to_check = os.path.join(DIRNAME, CHECK_DIRS)
    cmd = f"mypy --config-file {MYPY_CONFIG} {to_check}"
    print(cmd)
    ctx.run(cmd)


@task
def validate_pyproject_toml(ctx):
    project_file = os.path.join(DIRNAME, "pyproject.toml")
    cmd = f"validate-pyproject {project_file}"
    print(cmd)
    ctx.run(cmd)


@task
def pytest(ctx):
    os.environ["USE_REAL_DATASET_REGISTER"] = "No"
    cmd = f"pytest --color=yes {DIRNAME}"
    print(cmd)
    ctx.run(cmd)


@task
def pylint(ctx):
    rcfile = os.path.join(DIRNAME, "pylint.rc")

    with ctx.cd(DIRNAME):
        cmd = f"pylint --rcfile={rcfile} {CHECK_DIRS}"
        print(cmd)
        ctx.run(cmd)


@task(
    code_style,
    linters,
    mypy,
    validate_pyproject_toml,
    pylint,
    pytest,
)
def build(_):
    pass
