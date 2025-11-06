import pandas as pd
import numpy as np

print(pd.__version__)
print(np.__version__)

path = "data/uber_reviews.csv"
sampled_path = "data/uber_reviews_sampled.csv"
class Sampler:
    def __init__(self, data_path):

        self.data_path = data_path
        self.data = pd.read_csv(self.data_path, low_memory=False)
        self.total = len(self.data)  # total number of records in the dataset
        self.target_samples = 5000  # target number of samples
        self.stratify_column = "rating"  # column to stratify by

        print(f"Data loaded from {self.data_path}, total records: {len(self.data)}")
        print(self.data.head())

        self.data.info()

    #   add sampling method here
    #   random sample 5000 entries with stratifiying by rating
    """
    rating
    5    57.1% (611133)
    1    26.5% (283895)
    4     7.8% (82953)
    3     4.7% (49928)
    2     3.9% (41707)
    Name: proportion, dtype: object
    """

    def get_stratified_sample(self):
        stratified_sample = self.data.groupby(self.stratify_column).apply(
            lambda x: x.sample(n=int(len(x) / self.total * self.target_samples)),
            # include_groups=False
    )
        return stratified_sample
sampler = Sampler("data/uber_reviews.csv")



to_sample = input("Do you want to create a stratified sample of the data? (y/n): ")             

if to_sample == 'y':
    sampled = sampler.get_stratified_sample()
    sampled.to_csv("data/uber_reviews_sampled.csv", index=False)
    print("Original columns:", sampler.data.columns.tolist())
    print("Sampled columns:", sampled.columns.tolist())
    print("Stratified sample saved to data/uber_reviews_sampled.csv")
elif to_sample == 'n':
    sampled_data = pd.read_csv("data/uber_reviews_sampled.csv", low_memory=False)
    """
    debug to check sampled data matches original columns
    print("Original columns:", sampler.data.columns.tolist())
    print("Sampled columns:", sampled_data.columns.tolist())
    """
    
    print("Original data distribution:")
    print(sampler.data["rating"].value_counts())
    print("Sampled data distribution:")
    print(sampled_data["rating"].value_counts())
else:
    print("Invalid input, please enter 'y' or 'n'")
