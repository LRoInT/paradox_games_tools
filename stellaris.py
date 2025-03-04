import os
import sys
from p17t import stellaris
# 命令行 python stellaris.py [目标路径] [Stellaris 路径] [语言]
stellaris.copy_music(sys.argv[1],sys.argv[2],sys.argv[3],os.path.join(sys.argv[2],"localisation"),"music","dlc")