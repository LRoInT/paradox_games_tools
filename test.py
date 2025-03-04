localisation_dir="/mnt/win_program/Program Files/Stellaris/localisation/simp_chinese"

import os
import yaml



with open(os.path.join(localisation_dir, "achievements_l_simp_chinese.yml"),"r",encoding="utf-8") as f:
    lang = yaml.load(f, Loader=yaml.FullLoader)["l_simp_chinese"]
    print(lang)