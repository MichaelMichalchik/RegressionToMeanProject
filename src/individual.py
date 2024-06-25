class Individual:
    def __init__(self, id, intrinsic_value, extrinsic_value):
        self.id = id
        self.intrinsic_value = intrinsic_value
        self.extrinsic_value = extrinsic_value
        self.genetic_score = None
        self.environmental_score = None
        self.phenotype = self.calculate_phenotype(0.5)

    def calculate_phenotype(self, weight_genetic):
        self.genetic_score = self.intrinsic_value * weight_genetic
        self.environmental_score = self.extrinsic_value * (1 - weight_genetic)
        return self.genetic_score + self.environmental_score