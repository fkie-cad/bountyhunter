from yaml import dump, safe_load


def _save_data(path, data):
    with open(path, "w") as f:
        dump(data, f)


def _load_config(scenario, config_file, logger, load_config=True):
    if load_config:
        try:
            with open("plugins/bountyhunter/conf/" + scenario + config_file) as f:
                return safe_load(f)
        except FileNotFoundError:
            logger.warning(
                "Config file '{}' for scenario '{}' not found. Using default values.".format(config_file,
                                                                                             scenario))

    return {}