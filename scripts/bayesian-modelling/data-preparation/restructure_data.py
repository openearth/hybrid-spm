import pandas as pd

df = pd.read_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian_mwtl_dfm_cms.csv')

df=df.drop(columns=['Unnamed: 0'])

df.to_csv(r'P:\11206887-012-sito-is-2021-so-et-es\Data\input_bayesian\input_bayesian_mwtl_dfm_cms.csv')