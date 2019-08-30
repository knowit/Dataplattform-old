#!/usr/bin/env python

import sys
from ruamel.yaml import YAML
yaml = YAML()
yaml.preserve_quotes = True

# Oppdatere stage i gitt fil (serverless_file) til gitt stage (new_stage)
def change_stage(serverless_file, new_stage):

    #loader fil
    with open(serverless_file, 'r') as stream:
        data = yaml.load(stream)

        #oppdaterer data
        data['provider']['stage'] = new_stage

    #dumper data i fil
    with open(serverless_file, 'w') as stream:
        print("Oppdaterer "+serverless_file+"...")
        yaml.dump(data, stream)
        print("Stage byttet fra "+data['provider']['stage']+" til "+new_stage+" i "+serverless_file)


if __name__ == "__main__":

    try:
        serverless_file = sys.argv[1]
        new_stage = sys.argv[2]
        change_stage(serverless_file, new_stage)

    except IndexError:
        print("Trenger to parametere: <filename> <new stage>")








