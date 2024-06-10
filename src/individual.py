import numpy as np

class Individual:
    def __init__(self, id, intrinsic_value, extrinsic_value):
        self.id = id
        self.intrinsic_value = intrinsic_value
        self.extrinsic_value = extrinsic_value
        self.phenotype = self.calculate_phenotype(50)
    
    def calculate_phenotype(self, weight_genetic):
        weight_env = 100 - weight_genetic
        return (weight_genetic * self.intrinsic_value) + (weight_env * self.extrinsic_value)

