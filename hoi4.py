import os
import sys
from p17t import hoi4
# 命令行 python hoi4.py [目标路径] [HOI4 路径] [语言]
hoi4.copy_music(sys.argv[1],sys.argv[2],sys.argv[3],os.path.join(sys.argv[2],"localisation"),"music","dlc","integrated_dlc")