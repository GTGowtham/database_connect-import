import pandas as pd
import json
import sys
import os

script_dir=os.path.dirname(os.path.abspath(__file__))
project_root=os.path.dirname(script_dir)
data_path=os.path.join(project_root,'data','employees.csv')
output_path=os.path.join(project_root,"output")
print(output_path)


df=pd.read_csv(data_path)
save_json=os.path.join(output_path,'save_csv2json.json')
df.to_json(save_json, orient='records',indent=4,lines=True)


