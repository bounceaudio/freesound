import os

from invoke import task
from invoke.context import Context

DIRNAME = os.path.dirname(__file__)
MYPY_CONFIG = os.path.join(DIRNAME, "mypy.ini")


@task
def linters(ctx: Context) -> None:
    cmd = "ruff check"
    print(cmd)
    ctx.run(cmd)


@task
def code_style(ctx: Context) -> None:
    cmd = "ruff format --check"
    print(cmd)
    ctx.run(cmd)


@task
def mypy(ctx: Context) -> None:
    cmd = f"mypy --config-file {MYPY_CONFIG} {DIRNAME}"
    print(cmd)
    ctx.run(cmd)


@task
def validate_pyproject_toml(ctx: Context) -> None:
    project_file = os.path.join(DIRNAME, "pyproject.toml")
    cmd = f"validate-pyproject {project_file}"
    print(cmd)
    ctx.run(cmd)


@task
def pytest(ctx: Context) -> None:
    cmd = f"pytest --color=yes {DIRNAME}"
    print(cmd)
    ctx.run(cmd)


@task
def coverage(ctx: Context) -> None:
    cmd = f"pytest --cov={DIRNAME} --cov-report=xml --cov-report=term {DIRNAME}"
    print(cmd)
    ctx.run(cmd)


@task
def pylint(ctx: Context) -> None:
    rcfile = os.path.join(DIRNAME, "pylint.rc")

    with ctx.cd(DIRNAME):
        cmd = f"pylint --rcfile={rcfile} {DIRNAME}"
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
def build(_ctx: Context) -> None:
    pass
