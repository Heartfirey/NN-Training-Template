import os
import yaml
from utils import print, PrettyTable

__default_config_directory = os.path.join('.', 'config')


class YAMLParser(object):
    """Basic YAML parser class for config loading
    ! Noted that you should inherit this class and rewrite the config load function !
    Attributes:
        config_dir: the config storage directory, default setting to './config'
    """

    def __init__(self, config_dir="./config"):
        if not os.path.exists(config_dir):
            raise FileNotFoundError(f'Target directory({config_dir}) cannot be found!')
        self.config_dir = config_dir
        self.config_dict = dict()
        self.default_config = dict()

    def gen_template_cfg(self, cfg_name: str = 'template_cfg.yaml') -> None:
        """Generate a new configuration yaml and save it to configuration directory
        This operation will replace any file named with {cfg_name}
        :param cfg_name: template configuration file name, default set to "template_cfg"
        :return: None
        """
        yaml_path = os.path.join(self.config_dir, cfg_name)
        print(f'|INFO| Saving default config YAML files to directory: {yaml_path}', color='green')
        with open(yaml_path, encoding="utf-8", mode="w") as f:
            yaml.dump(self.default_config, stream=f, allow_unicode=True)

    def show_parameters(self) -> None:
        """Print all parameters
        This function will print all parameter to console
        :return: None
        """
        print("*-" * 10 + "*", color="yellow")
        print("|  Parameter Table  |", color="yellow")
        print("*-" * 10 + "*", color="yellow")
        parameter_table_list = list()  # Create a list for temporary storage
        parameter_table_list.append(('Global Parameters', PrettyTable(['ParameterName', 'ParameterValue'])))
        for parameter_name, parameter_value in self.config_dict.items():
            if isinstance(parameter_value, dict):
                current_table = PrettyTable(['ParameterName', 'ParameterValue'])
                for _parameter_name, _parameter_value in parameter_value.items():
                    current_table.add_row([_parameter_name, _parameter_value])
                parameter_table_list.append((parameter_name, current_table))
            else:
                parameter_table_list[0][1].add_row([parameter_name, parameter_value])  # Add to global parameter set
        for parameter_table_name, parameter_table in parameter_table_list:
            print('=>', parameter_table_name, color='red')
            print(parameter_table)

    def load_cfg(self, cfg_name: str) -> None:
        """Load the config from YAML file
        This function will load config from YAML files
        :param cfg_name: the file name of the config you want to load
        :return: None
        """
        cfg_file_directory = os.path.join(self.config_dir, cfg_name)
        if not os.path.exists(cfg_file_directory):
            raise FileNotFoundError(f'Target file({cfg_file_directory}) cannot be found!')
        if not os.path.isfile(cfg_file_directory):
            raise TypeError(f'Target directory({cfg_file_directory}) is not a file!')

        with open(cfg_file_directory, encoding="utf-8", mode="r") as f:
            config_read = yaml.load(stream=f, Loader=yaml.FullLoader)
            for parameter_name, default_value in self.default_config.items():
                if parameter_name not in config_read.keys():
                    config_read[parameter_name] = default_value
                else:
                    if isinstance(default_value, dict):
                        for _parameter_name, _default_value in default_value.items():
                            if _parameter_name not in config_read[parameter_name].keys():
                                config_read[parameter_name][_parameter_name] = _default_value
                            elif type(config_read[parameter_name][_parameter_name]) != type(_default_value):
                                raise TypeError(
                                    f"The type of parameter '{_parameter_name}' should be \
                                    {type(config_read[parameter_name][_parameter_name])}, \
                                    but got {type(_default_value)}")
            self.config_dict = config_read
    def register_parameter(self, p_name, default, p_type = None) -> None:
        """Register a parameter to default parameter dictionary
        :param p_type: parameter type, may be "train config" or "model config" etc.
        :param p_name: parameter name
        :param default: default value for this parameter
        :return: None
        """
        if p_type is None:
            self.default_config[p_name] = default
        else:
            if p_type not in self.default_config.keys():
                self.default_config[p_type] = dict()
            self.default_config[p_type][p_name] = default

    def __getitem__(self, key):
        """Get parameter values from storage dictionary
        :param key: parameter_name
        :return: parameter_value of given parameter_name
        """
        if key in self.config_dict.keys():
            return self.config_dict[key]
        else:
            self.config_dict[key] = dict()
            return self.config_dict[key]

    def __setitem__(self, key, value):
        """Set the parameter value
        :param key: parameter_name
        :param value: parameter_value
        :return: None
        """
        print(key, value)
        self.config_dict[key] = value
    # def get_param(self, ):


if __name__ == "__main__":
    test_paser = YAMLParser('E:\\PyCharmProjects\\NN-Training-Template\\config')
    # test_paser['name']['A'] = 1
    # test_paser['name']['B'] = 2
    # test_paser['train']['learing_rate'] = 0.01
    test_paser.register_parameter(p_type='train', p_name='lr', default=0.01)
    test_paser.register_parameter(p_type='train', p_name='momentum', default=0.1)
    test_paser.register_parameter(p_name='name', default='test_project')
    test_paser.register_parameter(p_name='version', default='v0.1')
    test_paser.register_parameter(p_name='test_none', default='tttt1')
    test_paser.register_parameter(p_type='train', p_name='test2', default='tttt2')
    # test_paser.gen_template_cfg()
    test_paser.load_cfg('template_cfg.yaml')
    test_paser.show_parameters()

