#-------------------------------------------------------------------------------
# DO NOT use `cpp_path=cpp`, which produces errors for headers transitively 
# included from Python.h.
#
# Configure cpp_args in ppconfig.yml.
#-------------------------------------------------------------------------------
import argparse

import yaml
from pycparser import parse_file


# preprocess the input file with given config
def cpp(filename, config):
    args = []
    with open('ppconfig.yml') as f:
        configs = yaml.load(f, Loader=yaml.FullLoader)
        # load the universal args for all projects
        for arg in configs.get('all'):
            args.append(arg)
        # load args for a specific project
        if config:
            if not configs.get(config):
                raise Warning("[ERROR] Unknown config name.")
            else:
                for opt in configs.get(config):
                    args.append(str(opt))
        # print(args)
        ast = parse_file(filename, use_cpp=True, cpp_path='gcc', cpp_args=args)
        return ast


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('filename', help='C file to be parsed')
    ap.add_argument('-c', '--config', 
        help='compilation options for specific project')
    ap.add_argument('-s', '--showcoord', 
        help='show coordinates in the dump', action='store_true')
    args = ap.parse_args()
    # print(args)

    try:
        ast = cpp(args.filename, args.config)
        ast.show(showcoord=args.showcoord)
    except Warning as w:
        print(w)
    except Exception as e:
        print(e)
        print("[ERROR] Preprocess failed, fix compilation options.")
