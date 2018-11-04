import none
import os
import config


if __name__ == '__main__':
    none.init(config)
    none.load_builtin_plugins()
    none.load_plugins(os.path.join(os.path.dirname(__file__), 'plugins'), 'plugins')
    none.run(host='127.0.0.1', port=8080)
