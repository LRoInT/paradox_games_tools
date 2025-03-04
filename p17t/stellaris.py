import json
import os
import shutil
from zipfile import ZipFile
import yaml
import tempfile
from .common import *
import atexit
import pprint

# Get musics and their names


def get_music_names(localisation_path, lang="english",localisation_list=[]):
    # Get music names from localisation files
    names = {}
    localisation_path = os.path.join(localisation_path, lang)
    with open(os.path.join(localisation_path, f"musicplayer_l_{lang}.yml"), "r", encoding="utf-8") as f:
        names.update(yaml.load(f.read(), Loader=yaml.FullLoader)[f"l_{lang}"])
    """for p in os.listdir(localisation_path): # 最坏的方法,
        if p.endswith(f"_l_{lang}.yml"):
            """
    for p in localisation_list:
        if os.path.exists(f:=os.path.join(localisation_path, f"{p}_l_{lang}.yml")):
            with open(f, "r", encoding="utf-8") as f:  # Check None YAML
                if not yaml.load(f.read(), Loader=yaml.FullLoader) is None:
                    f.seek(0)
                    if d := yaml.load(f.read(), Loader=yaml.FullLoader)[f"l_{lang}"]:
                        names.update(d)
    return names

def find_music(music_path):
    # 在目录中查找所有音乐文件 Find all music files in a directory
    music_list = {}
    for f in os.listdir(music_path):
        if f.endswith(".asset"):
            music_list.update(read_asset(os.path.join(music_path, f)))
        elif os.path.isdir(p := os.path.join(music_path, f)):
            music_list.update(find_music(p))
    return music_list

def find_all_music(default_music_path, *other):
    # 从游戏中搜索所有音乐 Find all music files in the game
    music_list = {}
    localisation_list = []
    # 默认音乐 Default music
    music_list.update(find_music(default_music_path))

    # 创建临时目录并自动清理 Create temp dir and Auto remove
    temp=tempfile.TemporaryDirectory()
    atexit.register(temp.cleanup)
    for i in other:  # For DLC music
        for f in os.listdir(i):
            if os.path.isdir(cf := os.path.join(i, f)):
                if (zf := f.split("_")[0]+".zip") in os.listdir(cf):
                    with ZipFile(os.path.join(i, f, zf)) as z:
                        fl = z.namelist()
                        if fl:
                            z.extractall(temp.name)
                            localisation_list.append(f[f.find("_")+1:])
    music_list.update(find_music(os.path.join(temp.name, "music")))
    return music_list, localisation_list


def copy_music(dir, game_path, lang, localisation, *music_path):
    # Copy music to a dir
    paths = [os.path.join(game_path, i) for i in music_path]
    music_list, localisation_list = find_all_music(*paths)
    pprint.pprint(music_list)
    pprint.pprint(localisation_list)
    music_names = get_music_names(localisation, lang, localisation_list)
    source = match_names(music_list, music_names)
    pprint.pprint(source)
    if not os.path.exists(dir):
        os.makedirs(dir)
    about_dict = {}
    for i in source:
        shutil.copy(i, os.path.join(dir, os.path.basename(i)))
        about_dict[os.path.basename(i)] = source[i]
    json.dump(about_dict, open(os.path.join(dir, "about.json"), "w"),
              ensure_ascii=False, indent=4)
