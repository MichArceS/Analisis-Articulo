import os
import json

with open("DM.json", 'r') as f:
    data = json.load(f)

final_dict = {}

for key in data:
    id_canal = data[key]
    for subdir, dirs, files in os.walk("Mensajes_Iria\\"):
        tmp = subdir.split("\\")[-1][1:]
        if str(id_canal) == tmp:
            with open(subdir + "\messages.json", 'r', encoding='utf-8') as f_2:
                data_2 = json.load(f_2)
                for element in data_2:
                    tmp_dict = {}
                    tmp_dict["Timestamp"] = element["Timestamp"]
                    tmp_dict["Content"] = element["Contents"]
                    final_dict[element["ID"]] = tmp_dict

print(len(final_dict))

with open("DM_messages.json", "w") as json_file:
    json.dump(final_dict, json_file, indent=4) # indent for pretty-printing
