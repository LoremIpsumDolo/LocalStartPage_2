from configparser import ConfigParser


def config(config_file="config.ini", section=None):
	# create a parser
	parser = ConfigParser(interpolation=None)
	# read config file
	parser.read(config_file)

	if not parser.has_section(section):
		raise Exception('Section {0} not found in the {1} file'.format(section, config_file))

	params = parser.items(section)
	return {param[0]: param[1] for param in params}
