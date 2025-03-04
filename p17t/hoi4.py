import json
import os
import shutil
import yaml
from ast import literal_eval
from .common import *

# Get musics and their names


def get_music_names(localisation_path, lang="english"):
    names = {}
    localisation_path = os.path.join(localisation_path, lang)
    for f in os.listdir(localisation_path):
        if f.endswith(f"music_l_{lang}.yml"):
            with open(os.path.join(localisation_path, f), "r", encoding="utf-8") as f:
                if not yaml.safe_load(f.read()) is None:
                    f.seek(0)
                    if d := yaml.safe_load(f.read())[f"l_{lang}"]:
                        names.update(d)
    return names


def find_all_music(music_path, *other):
    # Find all music files in the game
    music_list = {}

    # 默认音乐 Default music
    music_list.update(find_music(music_path))

    for i in other:  # DLC 音乐 For DLC music
        for f in os.listdir(i):
            if os.path.isdir(cf := os.path.join(i, f)):
                for f_1 in os.listdir(cf):
                    if f_1 == "music":
                        music_list.update(find_music(os.path.join(i, f, f_1)))
    return music_list


def copy_music(todir, game_path, lang, localisation, *music_path):
    # Copy music to a dir
    paths = [os.path.join(game_path, i) for i in music_path]
    music_list = find_all_music(*paths)
    music_names = get_music_names(localisation, lang)
    source = match_names(music_list, music_names)
    if not os.path.exists(todir):
        os.makedirs(todir)
    about_dict = {}
    for i in source:
        shutil.copy(i, os.path.join(todir, os.path.basename(i)))
        about_dict[os.path.basename(i)] = source[i]
    json.dump(about_dict, open(os.path.join(todir, "about.json"), "w"),
              ensure_ascii=False, indent=4)
