from neko_configparser import ConfigParserInterface

neko_config = ConfigParserInterface.parse_config()


def integrate():
    ConfigParserInterface.ensure_config(
        partition='daemonizer_dante',
        module_config={
            'pids_folder': f'{ConfigParserInterface.get_nekomata_folder()}/pids'
        }
    )
