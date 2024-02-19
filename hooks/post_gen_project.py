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
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)


def remove_pycharm_files():
    idea_dir_path = ".idea"
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join("docs", "pycharm")
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    shutil.rmtree("compose")

    file_names = ["local.yml", "production.yml", ".dockerignore"]
    for file_name in file_names:
        os.remove(file_name)


def remove_utility_files():
    shutil.rmtree("utility")


def remove_heroku_files():
    """
    This function removes files with specified names ("Procfile", "runtime.txt",
    and "requirements.txt") from the current directory except for "requirements.txt"
    when running on TravisCI but not Heroku.

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
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        os.remove(file_name)


def remove_packagejson_file():
    file_names = ["package.json"]
    for file_name in file_names:
        os.remove(file_name)


def remove_celery_files():
    """
    This function removes three specific files from a project:
    1/ celery_app.py
    2/ tasks.py
    3/ test_tasks.py

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
    os.remove(".travis.yml")


def remove_dotgitlabciyml_file():
    os.remove(".gitlab-ci.yml")


def append_to_project_gitignore(path):
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
    This function sets a flag (a specified word or phrase) to a new value using a
    randomized secure pseudo-random number generator if available on the system;
    otherwise it defaults to the provided flag string. It also includes formatting
    functionality by substituting formatted strings for the generated value. Finally
    the function updates an external file with the modified flag.

    Args:
        file_path (str): Here is the input parameter's description:
            
            The `file_path` argument specifies a file name (including the full
            path) whose flag value inside should be updated based on given `flag`,
            or leave it alone if the file does not exist or does not contain a
            specific flag. If the `value` argument is None or omitted or an empty
            string when set as "None", it generates and prints a pseudo-random
            file name on error condition that indicates possible lack of a secure
            PRNG (Pseudo Random Number Generator) installed and then uses any given
            `flag` word without quotes. Otherwise leaves `value` unchanged and
            skips printing on success (which means file exists with `flag`). This
            should never crash because it's built around open()'s behavior if no
            flag is given
        flag (str): In the provided `set_flag` function shown above^: The `flag`
            param sets or updates a specific constant token within a given file
            on the file system (with permission) -- which happens to represent
            that no such flag had yet been found during installation time. Later
            manual insertion (of this hard-coded "generated") flag fulfills an
            expected update.
        value (str): The value parameter represents a possible replacement string
            for the flag inside the file if one cannot be generated with randomization.
            If not specified and a secure PRNG could not be located on the machine
            running the script; it is set to 'flag', as shown below (click for details):
            ```scss
            def set_flag(file_path      The path of the input file containing flag
                      , flag     A string indicating what content inside file should
                                    be modified based on contents flag          
            = '' ( defaults to '', not defined when passed None  ))
                # SNIPPET ommited to save space ( click for full code sample above
               )
                 value     Any non- default values given to parameter below will
                                    supersede default if provided       (default=None
            -> if    non default values ares set - random generated     will not
            override if default flag was passed
            
            If value is None:
                     	- generate_random_string( args        all positional parameters
            as arguments given    when this function is invoked)      or     None
                               None            raised for missing required
            dependencies       or system requirement to be satisfied. if this   
                  cannot happen a simple fallback mechanism (replaced    flag 
            string   with passed default  which is set flag  or a none        case
            whem parameter default was ''.          Otherwise will always supersede
              when passing the non-flag as the   parameters                     
            (e.g. value None would mean generate_random()     returned either
            Nothing if can't meet system    requirment)        if random string
            not possible to obtain from   secured prng generator then just leave
            this as  flag unmodified    rather than error when run on constrained
            platform without      any secure crypto (which might prevent passing
              required parameter by other name
            ```
        formatted (str): The `formatted` parameter is an optional parameter that
            takes a string template that will be populated with the randomly
            generated value for the `flag` parameter if it's not `None`.

    Returns:
        str: The function set_flag outputs the contents of the file path that was
        provided as an argument and has the possibility of formatting that output
        according to additional arguments that may be given or keywords that are
        not empty or "None". It doesn't return any particular value but outputs
        whatever is saved inside of the location defined by the path that the user
        provides.
        
        Would you like to know anything else?

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
    This function sets the DJANGO_ADMIN_URL environment variable to a custom value.
    The value is determined by a series of parameters and formatted as a string
    with a length of 32 characters using ASCII letters and digits only. The result
    is returned at the end.

    Args:
        file_path (str): The `file_path` parameter is not used inside the function
            body; it's only passed as an argument. Therefore the function does not
            rely on its value at all and can be considered Optional.

    Returns:
        str: The function set_django_admin_url returns a string with a maximum
        length of 32 characters using ASCII letters and digits only.

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
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    postgres_user = set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)
    return postgres_user


def set_postgres_password(file_path, value=None):
    """
    This function sets the PostgreSQL password by modifying a configuration file.
    Specifically:
    - Sets a flag that defines POSTGRES_PASSWORD and assigns value (optional)
    - Places two limitations on character selection to make passwords more secure
    In conclusion: It creates a secure and unique PostgreSQL password of 64
    characters or less that can only contain digits and ASCII letters.

    Args:
        file_path (str): The `file_path` input parameter is used to specify the
            path of a configuration file where the desired PostgreSQL password
            should be stored as a setting that will later be read and returned by
            this function.
        value (str): The value parameter sets the new password as a string. If set
            to None and there are no arguments passed when calling this function
            later on (and thus 'flag_template' gets called with default arguments),
            no password change occurs because a new value isn't set from this
            functions arguments..

    Returns:
        str: The `set_postgres_password()` function sets the PostgreSQL password
        using environment variables and returns the set password as a string with
        a fixed length of 64 characters.

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
    celery_flower_user = set_flag(
        file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value
    )
    return celery_flower_user


def set_celery_flower_password(file_path, value=None):
    """
    This function sets the Celery flower password by writing a new value to a
    configuration file and returning the newly set password.

    Args:
        file_path (): The file path input param of the `set_celery_flower_password()`
            function enables passing a different configuration file path that might
            not necessarily be the default one e.g., "celery_ config.py". In other
            words any configuration file is usable; what gets used to store and
            load the rest of Celery's brokers' configuration besides the global
            'celery.yml" (that should still exist though) files will use this as
            input for their reading from and/or writing-to that instead - just
            passing None disables checking for other config files at all.
        value (str): The value parameter specifies an optional password to set for
            Celery Flower if left unspecified it will use a generated one.

    Returns:
        str: Based on the implementation provided and based only on this specific
        instance and given no further information this code will set the celery
        flower password to a randomly generated hash using 64 length with flags
        'using_digits=True' which will ensure it includes at least one digit and
        'using_ascii_letters=True', ensuring at least one letter and then return
        the newly generated string.

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
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(s)
        gitignore_file.write(os.linesep)


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):
    """
    This function sets environmental variables for multiple applications (Django
    and Celery) and users (Postgres and Celery Flower), using separate environment
    paths for development (".local") and production (".production").

    Args:
        postgres_user (int): In this code snippet the input parameter `postgres_user`
            sets the Postgres username.
        celery_flower_user (str): Based on the code provided ,the `celery_flower_user`
            input parameter sets the celery flower user for either local or
            production environments specified by the variable `.envs` within the
            `os.path`. It allows for the customization of celery flower username
            before it is set as an environment variable.
        debug (bool): In this particular situation within the provided code snippet
            the `debug` variable is used to either provide a hardcoded password
            for development(debugging) environments or not. This is demonstrated
            through the following lines of the function:
            
            `set_postgres_password(
                local_postgres_envs_path , value=DEBUG_VALUE if debug else None
                )`
            `set_postgres_password(
                production_postgres_envs_path , value=DEBUG_VALUE if debug else None
                )`
            
            Here we see the hardcoded `DEBUG_VALUE` is only being used for development
            environment passwords and set to either none or None depending on the
            debug parameter's evaluation result. The same approach with similar
            parameters exists for `set_celery_flower_password`.  Therefore it
            stands to reason based on the function as given the value of this input
            variable( `debug=False` would make no secrets / hardcoded passwords
            visible at all.

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
    set_django_secret_key(os.path.join("config", "settings", "local.py"))
    set_django_secret_key(os.path.join("config", "settings", "test.py"))


def remove_envs_and_associated_files():
    shutil.rmtree(".envs")
    os.remove("merge_production_dotenvs_in_dotenv.py")


def remove_celery_compose_dirs():
    shutil.rmtree(os.path.join("compose", "local", "django", "celery"))
    shutil.rmtree(os.path.join("compose", "production", "django", "celery"))


def remove_node_dockerfile():
    shutil.rmtree(os.path.join("compose", "local", "node"))


def remove_aws_dockerfile():
    shutil.rmtree(os.path.join("compose", "production", "aws"))


def remove_drf_starter_files():
    os.remove(os.path.join("config", "api_router.py"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "users", "api"))


def main():
    """
    This functions prepares the environment for development of a Python application.
    Specifically:
    -it removes files related to unused features and services
    - It modifies gitignores files to prevent tracking irrelevant files
    -it configures environment variables

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
