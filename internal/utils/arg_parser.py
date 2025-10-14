import logging

from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def create_agr_parser(parser,
                      arg_name,
                      action="store",
                      nargs=None,
                      const=None,
                      default=None,
                      variable_type=str,
                      choices=None,
                      required=False,
                      help_text=None,
                      metavar=None,
                      dest=None):
    """ Create new argparse.ArgumentParser with one add_argument, it uses library argparse, the most of args are same Look at documentation
        :param parser: enter parser (argparse.ArgumentParser)
        :param arg_name: name of arg "file" or --file (["--file", "-f"])
        :param action: what is to happen while entering arg ("store", "store_true", "store_false", ...)
        :param nargs: Amount of the args (None, "?", "+", ...)
        :param const: Const value for action store_const
        :param default: default value if user didn't enter arg
        :param variable_type: data type (int, str, ...)
        :param choices: Accessible values ["red", "green"]
        :param required: if the arg is required
        :param help_text: text in the help (--help)
        :param metavar: name in the help instead variable name
        :param dest: name of the attribute
        :return argparse.ArgumentParser with add_argument"""

    try:
        parser.add_argument(
            *arg_name,
            action=action,
            nargs=nargs,
            const=const,
            default=default,
            type=variable_type,
            choices=choices,
            required=required,
            help=help_text,
            metavar=metavar,
            dest=dest,
        )
    except Exception as e:
        logger.error(f"Error while trying to add argument... {str(e)}")
        return None

    return parser.parse_args()