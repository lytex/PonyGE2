from fitness.base_ff_classes.base_ff import base_ff
import subprocess
import numpy as np
from algorithm.parameters import params
from fitness.supervised_learning.supervised_learning import supervised_learning
from utilities.fitness.error_metric import Hamming_error


class strudel(base_ff):
    """
    Fitness function class for minimising the number of nodes in a
    derivation tree.
    """

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
        if params['ERROR_METRIC'] is None:
            params['ERROR_METRIC'] = Hamming_error

        self.maximise = params['ERROR_METRIC'].maximise

        data = np.genfromtxt("../datasets/" + params["DATASET_TRAIN"], delimiter="\t", skip_header=True)
        y = data[:, 1]
        self.y = y.astype("uint8")

    def evaluate(self, ind, **kwargs):
        length = len(self.y)
        js_code = """ import { evaluate_mini } from "./evaluate.mjs";""" \
        f"""let mini_code = "{ind.phenotype}";
        console.log(evaluate_mini(mini_code, {length}).join("\\n")); """
        with open("../../scratchpad.mjs", "w") as f:
            f.write(js_code)
        result = subprocess.check_output("node ../../scratchpad.mjs", shell=True, stderr=subprocess.DEVNULL)
        yhat = np.array([int(x) for x in result.decode('utf-8').replace('🌀 @strudel/core loaded 🌀\n', '').split('\n') if x])
        print(ind.phenotype)
        print(yhat)
        print(self.y)
        error = np.sum(np.abs(self.y-yhat))
        # + 0.5*len(ind.genome)
        print(error)
        return error



