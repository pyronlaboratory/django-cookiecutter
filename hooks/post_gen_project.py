"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"

def remove_open_source_files():
    """
    removes specified open-source files from a codebase by naming them and invoking
    the `os.remove()` method for each named file.

    """
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        os.remove(file_name)

def remove_gplv3_files():
    """
    removes files with specified names from a given path.

    """
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)

def remove_pycharm_files():
    """
    removes two directories related to PyCharm, namely `.idea` and `docs/pycharm`.

    """
    idea_dir_path = ".idea"
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join("docs", "pycharm")
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    """
    deletes the directory `compose`, and then removes files with names `local.yml`,
    `production.yml`, and `.dockerignore`.

    """
    shutil.rmtree("compose")

    file_names = ["local.yml", "production.yml", ".dockerignore"]
    for file_name in file_names:
        os.remove(file_name)


def remove_utility_files():
    """
    removes the 'utility' directory and its contents using the `shutil.rmtree()`
    method.

    """
    shutil.rmtree("utility")


def remove_heroku_files():
    """
    removes specified files from the current directory if certain conditions are
    met. It checks the file name and contents to determine whether it should be
    removed when using Travis CI but not Heroku.

    """
    file_names = ["Procfile", "runtime.txt", "requirements.txt"]
    for file_name in file_names:
        if (
            file_name == "requirements.txt"
            and "{{ cookiecutter.ci_tool }}".lower() == "travis"
        ):
            # don't remove the file if we are using travisci but not using heroku
            continue
        os.remove(file_name)


def remove_gulp_files():
    """
    removes files with specified names from the system, ignoring any potential errors.

    """
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        os.remove(file_name)


def remove_packagejson_file():
    """
    removes specified files from a system.

    """
    file_names = ["package.json"]
    for file_name in file_names:
        os.remove(file_name)


def remove_celery_files():
    """
    removes celery files in a specific location, including `config/celery_app.py`,
    `{{ cookiecutter.project_slug }}/users/tasks.py`, and `{{ cookiecutter.project_slug
    }}/users/tests/test_tasks.py`.

    """
    file_names = [
        os.path.join("config", "celery_app.py"),
        os.path.join("{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        os.path.join(
            "{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"
        ),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_dottravisyml_file():
    """
    removes a configuration file with the name ".travis.yml" from the system.

    """
    os.remove(".travis.yml")


def remove_dotgitlabciyml_file():
    """
    removes the `.gitlab-ci.yml` file from the current directory.

    """
    os.remove(".gitlab-ci.yml")


def append_to_project_gitignore(path):
    """
    adds a file path to the project's `.gitignore` file in the current working
    directory, separating them with an OS line break.

    Args:
        path (str): path to be added to the project's .gitignore file.

    """
    gitignore_file_path = ".gitignore"
    with open(gitignore_file_path, "a") as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    """
    modifies a file's contents by replacing a specified string (the `flag`) with
    a new value (the `value`). It also generates a pseudo-random string when no
    value is provided and formatting is required.

    Args:
        file_path (str): path to the file that the function will write or read from.
        flag (str): string that should be replaced by a randomly generated
            pseudo-random number, which is then written back to the specified file
            path.
        value (`object` in the `def` function.): new value to replace the specified
            `flag` in the file contents.
            
            		- If `value` is `None`, it indicates that a secure pseudo-random
            number generator was not found on the system, and manual intervention
            may be necessary to set the flag.
            		- The ` formatted` parameter, if provided, allows for formatting of
            the random string generated when `value` is set to `None`. The formatting
            is done using the provided formatting string, which is a Python
            formatting string.
            		- The `file_path` parameter specifies the path to the file where the
            flag will be written.
            		- The `flag` parameter indicates the flag being set.
            
            	These properties of `value` provide additional context for its use
            in the function.
        formatted (str): format string that will be used to replace the `flag`
            with its value if it is not `None`.

    Returns:
        str: a modified version of the original file contents with the specified
        flag replaced by a pseudo-random string.

    """
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    """
    sets a Django secret key for use in settings.py based on the input file path
    provided.

    Args:
        file_path (str): file path where the Django secret key is stored and will
            be read by the function.

    Returns:
        str: a generated Django secret key consisting of 64 digits, using both
        uppercase and lowercase letters.

    """
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key

def set_django_admin_url(file_path):
    """
    sets a flag in a file to define the Django administration URL prefix using a
    format string with digits and ASCII letters, returning the modified URL prefix.

    Args:
        file_path (str): 32-digit hexadecimal code for the Django admin URL.

    Returns:
        str: a pre-formatted URL for the Django administration interface.

    """
    django_admin_url = set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_admin_url

def generate_random_user():
    """
    generates a 32-character random string using ASCII letters only.

    Returns:
        str: a 32-character string of random ASCII letters.

    """
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    """
    generates a PostgreSQL user account with a unique name and password, using
    either the `DEBUG_VALUE` or a randomly generated string for creation when
    `debug` is `False`.

    Args:
        debug (bool): state of generating high-quality documentation

    Returns:
        str: a randomized string of letters and digits for a PostgreSQL user.

    """
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    """
    sets a environment variable related to PostgreSQL users.

    Args:
        file_path (str): path to the configuration file where the Postgres user
            setting is stored.
        value (str): new PostgreSQL user to set.

    Returns:
        str: a string indicating whether the PostgreSQL user was set successfully
        or not.

    """
    postgres_user = set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)
    return postgres_user


def set_postgres_password(file_path, value=None):
    """
    sets a password for PostgreSQL using environment variable settings.

    Args:
        file_path (str): file path where the PostgreSQL password is stored.
        value (int): 64-character PostgreSQL password to be set, with the requirement
            that it contains only ASCII letters and must be exactly 64 characters
            long.

    Returns:
        str: a securely stored PostgreSQL password.

    """
    postgres_password = set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return postgres_password


def set_celery_flower_user(file_path, value):
    """
    sets a flag in a file path with a specific key to set the Celery flower user
    to the provided value.

    Args:
        file_path (str): file path where the Celery flower user setting should be
            written or read from.
        value (str): new value of the `celery_flower_user` flag that should be set
            for the given file path.

    Returns:
        `set` value.: a boolean value indicating whether the `celery_flower_user`
        flag has been set to the provided value.
        
        		- `celery_flower_user`: The value set for the `CELERY_FLOWER_USER`
        environment variable. This is an atomic property, which means it can only
        have one of two possible values: either `True` or `False`.
        		- `file_path`: The path to the file where the flag was set. This property
        is also atomic and has a value that is either a string or null.

    """
    celery_flower_user = set_flag(
        file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value
    )
    return celery_flower_user


def set_celery_flower_password(file_path, value=None):
    """
    sets a password for Celery Flowers using a file path and a specified value.

    Args:
        file_path (str): file path where the CELERY_FLOWER_PASSWORD flag is stored.
        value (int): 64-digit password to be set for Celery Flower, and it is used
            by the `set_flag()` function to store the password in the file path provided.

    Returns:
        str: a password for Celery Flower.

    """
    celery_flower_password = set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return celery_flower_password


def append_to_gitignore_file(s):
    """
    adds a given string to the end of the `.gitignore` file.

    Args:
        s (str): string of lines to be appended to the `.gitignore` file.

    """
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(s)
        gitignore_file.write(os.linesep)


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):
    """
    sets environment variables for Django and PostgreSQL users, passwords, and
    Celery Flower user, depending on whether the environment is local or production.

    Args:
        postgres_user (str): PostgreSQL user account name to be set for the local
            environment and the production environment respectively in the function
            `set_flags_in_envs`.
        celery_flower_user (str): user name for Celery flower, which is used to
            set the user name for Celery flower instance in the production environment.
        debug (bool): Debug Value, which is used to set the secret key, admin URL,
            PostgreSQL user and password, and Celery Flower user and password
            accordingly in the local and production environments, with different
            values being set when `debug` is True or False.

    """
    local_django_envs_path = os.path.join(".envs", ".local", ".django")
    production_django_envs_path = os.path.join(".envs", ".production", ".django")
    local_postgres_envs_path = os.path.join(".envs", ".local", ".postgres")
    production_postgres_envs_path = os.path.join(".envs", ".production", ".postgres")

    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)

    set_postgres_user(local_postgres_envs_path, value=postgres_user)
    set_postgres_password(
        local_postgres_envs_path, value=DEBUG_VALUE if debug else None
    )
    set_postgres_user(production_postgres_envs_path, value=postgres_user)
    set_postgres_password(
        production_postgres_envs_path, value=DEBUG_VALUE if debug else None
    )

    set_celery_flower_user(local_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(
        local_django_envs_path, value=DEBUG_VALUE if debug else None
    )
    set_celery_flower_user(production_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(
        production_django_envs_path, value=DEBUG_VALUE if debug else None
    )


def set_flags_in_settings_files():
    """
    sets the Django secret key in settings files located at `config/settings/local.py`
    and `config/settings/test.py`.

    """
    set_django_secret_key(os.path.join("config", "settings", "local.py"))
    set_django_secret_key(os.path.join("config", "settings", "test.py"))


def remove_envs_and_associated_files():
    """
    removes the `.envs` directory and the file `merge_production_dotenvs_in_dotenv.py`.

    """
    shutil.rmtree(".envs")
    os.remove("merge_production_dotenvs_in_dotenv.py")


def remove_celery_compose_dirs():
    """
    removes two directory paths related to Celery.

    """
    shutil.rmtree(os.path.join("compose", "local", "django", "celery"))
    shutil.rmtree(os.path.join("compose", "production", "django", "celery"))


def remove_node_dockerfile():
    """
    removes the directory `os.path.join("compose", "local", "node")`.

    """
    shutil.rmtree(os.path.join("compose", "local", "node"))


def remove_aws_dockerfile():
    """
    removes the directory `os.path.join("compose", "production", "aws")

    """
    shutil.rmtree(os.path.join("compose", "production", "aws"))


def remove_drf_starter_files():
    """
    removes files related to the Django Rest Framework (DRF) starter project from
    a directory. Specifically, it removes the `api_router.py` file and deletes the
    `users` directory containing the DRF project structure.

    """
    os.remove(os.path.join("config", "api_router.py"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "users", "api"))


def main():
    """
    initializes a project based on cookiecutter parameters, removes unnecessary
    files and configures GIT ignores to preserve locally useful files.

    """
    debug = "{{ cookiecutter.debug }}".lower() == "y"

    set_flags_in_envs(
        DEBUG_VALUE if debug else generate_random_user(),
        DEBUG_VALUE if debug else generate_random_user(),
        debug=debug,
    )
    set_flags_in_settings_files()

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.use_pycharm }}".lower() == "n":
        remove_pycharm_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        remove_utility_files()
    else:
        remove_docker_files()

    if (
        "{{ cookiecutter.use_docker }}".lower() == "y"
        and "{{ cookiecutter.cloud_provider}}".lower() != "aws"
    ):
        remove_aws_dockerfile()

    if "{{ cookiecutter.use_heroku }}".lower() == "n":
        remove_heroku_files()

    if (
        "{{ cookiecutter.use_docker }}".lower() == "n"
        and "{{ cookiecutter.use_heroku }}".lower() == "n"
    ):
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            print(
                INFO + ".env(s) are only utilized when Docker Compose and/or "
                "Heroku support is enabled so keeping them does not "
                "make sense given your current setup." + TERMINATOR
            )
        remove_envs_and_associated_files()
    else:
        append_to_gitignore_file(".env")
        append_to_gitignore_file(".envs/*")
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            append_to_gitignore_file("!.envs/.local/")

    if "{{ cookiecutter.js_task_runner}}".lower() == "none":
        remove_gulp_files()
        remove_packagejson_file()
        if "{{ cookiecutter.use_docker }}".lower() == "y":
            remove_node_dockerfile()

    if "{{ cookiecutter.cloud_provider}}".lower() == "none":
        print(
            WARNING + "You chose not to use a cloud provider, "
            "media files won't be served in production." + TERMINATOR
        )

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()
        if "{{ cookiecutter.use_docker }}".lower() == "y":
            remove_celery_compose_dirs()

    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        remove_dottravisyml_file()

    if "{{ cookiecutter.ci_tool }}".lower() != "gitlab":
        remove_dotgitlabciyml_file()

    if "{{ cookiecutter.use_drf }}".lower() == "n":
        remove_drf_starter_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
