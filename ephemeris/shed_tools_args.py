"""This file contains the parser for shed_tools"""

from argparse import ArgumentParser
from .common_parser import get_common_args

def parser():
    """construct the parser object"""
    common_arguments = get_common_args(log_file=True)
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    # A list of defaults is needed. Otherwise the shed-tools install parser will not return
    # update_tools in the name space and shed-tool update will not return all the install
    # variables.
    parser.set_defaults(
        action="install",
        tool_list_file=None,
        tool_yaml=None,
        owner=None,
        name=None,
        tool_panel_section_id=None,
        tool_panel_section_label=None,
        revisions=None,
        tool_shed_url=None,
        skip_tool_dependencies=False,
        install_resolver_dependencies=False,
        force_latest_revision=False,
        test=False,
        test_user_api_key=None,
        test_user="ephemeris@galaxyproject.org",
        test_json="tool_test_output.json",
        test_existing=False,
    )
    install_command_parser = subparsers.add_parser(
        "install",
        help="This installs tools in Galaxy from the Tool Shed."
             "Use shed-tools install --help for more information",
        parents=[common_arguments],
    )
    update_command_parser = subparsers.add_parser(
        "update",
        help="This updates all tools in Galaxy to the latest revision. "
             "Use shed-tools update --help for more information",
        parents=[common_arguments])

    test_command_parser = subparsers.add_parser(
        "test",
        help="This tests the supplied list of tools in Galaxy. "
             "Use shed-tools test --help for more information",
        parents=[common_arguments])

    for command_parser in [install_command_parser, test_command_parser]:
        command_parser.add_argument(
            "-t", "--toolsfile",
            dest="tool_list_file",
            help="Tools file to use (see tool_list.yaml.sample)",)
        command_parser.add_argument(
            "-y", "--yaml_tool",
            dest="tool_yaml",
            help="Install tool represented by yaml string",)
        command_parser.add_argument(
            "--name",
            help="The name of the tool to install (only applicable "
                 "if the tools file is not provided).")
        command_parser.add_argument(
            "--owner",
            help="The owner of the tool to install (only applicable "
                 "if the tools file is not provided).")
        command_parser.add_argument(
            "--revisions",
            default=None,
            nargs='*',
            dest="revisions",
            help="The revisions of the tool repository that will be installed. "
                 "All revisions must be specified after this flag by a space."
                 "Example: --revisions 0a5c7992b1ac f048033da666"
                 "(Only applicable if the tools file is not provided).")
        command_parser.add_argument(
            "--toolshed",
            dest="tool_shed_url",
            help="The Tool Shed URL where to install the tool from. "
                 "This is applicable only if the tool info is "
                 "provided as an option vs. in the tools file.")

    install_command_parser.add_argument(
        "--section",
        dest="tool_panel_section_id",
        help="Galaxy tool panel section ID where the tool will "
             "be installed (the section must exist in Galaxy; "
             "only applicable if the tools file is not provided).")
    install_command_parser.add_argument(
        "--section_label",
        default=None,
        dest="tool_panel_section_label",
        help="Galaxy tool panel section label where tool will be installed "
             "(if the section does not exist, it will be created; "
             "only applicable if the tools file is not provided).")
    install_command_parser.add_argument(
        "--skip_install_tool_dependencies",
        action="store_true",
        dest="skip_tool_dependencies",
        help="Skip the installation of tool dependencies using classic toolshed packages. "
             "Can be overwritten on a per-tool basis in the tools file.")
    install_command_parser.add_argument(
        "--install_resolver_dependencies",
        action="store_true",
        dest=""
             "",
        help="Install tool dependencies through resolver (e.g. conda). "
             "Will be ignored on galaxy releases older than 16.07. "
             "Can be overwritten on a per-tool basis in the tools file")
    install_command_parser.add_argument(
        "--latest",
        action="store_true",
        dest="force_latest_revision",
        help="Will override the revisions in the tools file and always install the latest revision.")

    for command_parser in [update_command_parser, install_command_parser]:
        command_parser.add_argument(
            "--test",
            action="store_true",
            dest="test",
            help="Run tool tests on install tools, requires Galaxy 18.05 or newer."
        )
        command_parser.add_argument(
            "--test_existing",
            action="store_true",
            help="If testing tools during install, also run tool tests on repositories already installed "
                 "(i.e. skipped repositories)."
        )
        command_parser.add_argument(
            "--test_json",
            dest="test_json",
            help="If testing tools, record tool test output to specified file. "
                 "This file can be turned into reports with ``planemo test_reports <output.json>``."
        )
        command_parser.add_argument(
            "--test_user_api_key",
            dest="test_json",
            help="If testing tools, a user is needed to execute the tests. "
                 "This can be different the --api_key which is assumed to be an admin key. "
                 "If --api_key is a valid user (e.g. it is not a master API key) this does "
                 "not need to be specified and --api_key will be reused."
        )
        command_parser.add_argument(
            "--test_user",
            dest="test_json",
            help="If testing tools, a user is needed to execute the tests. "
                 "If --api_key is a master api key (i.e. not tied to a real user) and "
                 "--test_user_api_key isn't specified, this user email will be used. This "
                 "user will be created if needed."
        )

    # Same test_json as above but language modified for test instead of install/update.
    test_command_parser.add_argument(
        "--test_json",
        dest="test_json",
        help="Record tool test output to specified file. "
             "This file can be turned into reports with ``planemo test_reports <output.json>``."
    )

    test_command_parser.add_argument(
        "--test_user_api_key",
        dest="test_user_api_key",
        help="A user is needed to execute the tests. "
             "This can be different the --api_key which is assumed to be an admin key. "
             "If --api_key is a valid user (e.g. it is not a master API key) this does "
             "not need to be specified and --api_key will be reused."
    )
    test_command_parser.add_argument(
        "--test_user",
        dest="test_user",
        help="A user is needed to execute the tests. "
             "If --api_key is a master api key (i.e. not tied to a real user) and "
             "--test_user_api_key isn't specified, this user email will be used. This "
             "user will be created if needed."
    )

    update_command_parser.set_defaults(
        action="update"
    )

    test_command_parser.set_defaults(
        action="test"
    )

    return parser
