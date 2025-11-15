import pandas as pd
import os
script_dir=os.path.dirname(os.path.abspath(__file__))
project_root=os.path.dirname(script_dir)
data_path=os.path.join(project_root,'data','employees.csv')
output_path=os.path.join(project_root,"output")

# print(output_path)
df=pd.read_csv(data_path)

def convert_row(row):
      return"""
      <id="%s">
      <name>%s</name>
      <email>%s</email>
      <department>%s</department>
      </id>
""" %(row["id"],row["name"],row["email"],row["department"])

save_xml=os.path.join(output_path,'save_csv2xml.xml')
with open(save_xml,'w') as f:
      f.write("<employees>")
      for index,row in df.iterrows():
            f.write(convert_row(row))
      f.write("</employees>")



# df=pd.read_csv(data_path)
# save_xml=os.path.join(output_path,'save_csv2xml.xml')
# df.to_xml(save_xml,index=False)
