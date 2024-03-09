from fitness.base_ff_classes.base_ff import base_ff
import subprocess


class strudel(base_ff):
    """
    Fitness function class for minimising the number of nodes in a
    derivation tree.
    """

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        js_code = """ import { evaluate_mini } from "./evaluate.mjs";""" \
        f"""let mini_code = "{ind.phenotype}";
        console.log(evaluate_mini(mini_code, 4).join("\\n")); """
        with open("../../scratchpad.mjs", "w") as f:
            f.write(js_code)
        result = subprocess.check_output("node ../../scratchpad.mjs", shell=True, stderr=subprocess.DEVNULL)
        midi = [int(x) for x in result.decode('utf-8').replace('🌀 @strudel/core loaded 🌀\n', '').split('\n') if x]
        print(midi)

        return ind.nodes



