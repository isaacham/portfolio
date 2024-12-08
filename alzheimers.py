import pandas as pd
from chembl_webresource_client.new_client import new_client
import os

## README
# 1. Will look into ChEMBL database and look for alzheimer's, download bioactivity data
# 2. Preprocess bioactivity data and output a preprocess version


# Editing directory
# cwd = os.getcwd()
# print(cwd)

# output = "/Users/admin/"
# os.chdir(output)
# print(f"New Working Directory: {os.getcwd()}")


# Target search for HH (Hereditary Hemochromatosis)

target = new_client.target
target_query = target.search('alzheimers')
targets = pd.DataFrame.from_dict(target_query)

targets

 # Select and Retrieve Bioactivity data for Alzheimers

selected_target = targets.target_chembl_id[5]
selected_target

# We will retrieve bioactivity data for amyloid-beta protein

activity = new_client.activity 
res = activity.filter(target_chembl_id=selected_target).filter(standard_type = "EC50")

df = pd.DataFrame.from_dict(res)

df.to_csv('bioactivity_data.csv', index=False)

# Handling missing data

df2 = df[df.standard_value.notna()]

# Data preprocessing

bioactivity_class = []

for i in df2.standard_value:
    if float(i) >= 10000:
        bioactivity_class.append('inactive')
    elif float(i) <= 10000:
        bioactivity_class.append('active')
    else:
        bioactivity_class.append('intermediate')
        
# Iteration over mol_cid, canonical smiles, standard value

mol_cid = []
for i in df2.molecule_chembl_id:
    mol_cid.append(i)

canonical_smiles = []
for i in df2.molecule_chembl_id:
    canonical_smiles.append(i)

standard_value = []
for i in df2.molecule_chembl_id:
    standard_value.append(i)
    
    
selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2[selection] # Storing Data Selections into a dataframe
pd.concat([df3,pd.Series(bioactivity_class)], axis=1)

# Save DataFrame into a .csv file

df3.to_csv('bioactivity_preprocessed_data.csv', index=False)