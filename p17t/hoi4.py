import json
import os
import shutil
import yaml
from ast import literal_eval

# Get musics and their names


def read_asset(file_path):
    # Read Assert file to get music and its key
    music_list = {}
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("name"):
                n = ""
                s = False
                for i in line[5:]:
                    if i == '"':
                        if s:
                            break
                        s = True
                    else:
                        if s:
                            n += i
            elif line.startswith("file"):
                f = ""
                s = False
                for i in line[5:]:
                    if i == '"':
                        if s:
                            break
                        s = True
                    else:
                        if s:
                            f += i
                music_list[n] = os.path.join(os.path.dirname(file_path), f)
    return music_list


def get_music_names(localisation_path, lang="english"):
    names = {}
    localisation_path = os.path.join(localisation_path, lang)
    for f in os.listdir(localisation_path):
        if f.endswith(f"music_l_{lang}.yml"):
            with open(os.path.join(localisation_path, f), "r", encoding="utf-8") as f:
                names.update(
                    yaml.load(f.read(), Loader=yaml.FullLoader)[f"l_{lang}"])
    return names


def find_music(music_path):
    # Find all music files in a directory
    music_list = {}
    for f in os.listdir(music_path):
        if f.endswith(".asset") and "music" in f:
            music_list.update(read_asset(os.path.join(music_path, f)))
        elif os.path.isdir(p := os.path.join(music_path, f)):
            music_list.update(find_music(p))
    return music_list


def find_all_music(music_path, *other):
    # Find all music files in the game
    music_list = {}

    # Default music
    music_list.update(find_music(music_path))

    for i in other:  # For DLC music
        for f in os.listdir(i):
            if os.path.isdir(cf := os.path.join(i, f)):
                for f_1 in os.listdir(cf):
                    if f_1 == "music":
                        music_list.update(find_music(os.path.join(i, f, f_1)))
    return music_list


def match_names(music_list, names):
    match = {}
    for i in names:
        if i in music_list:
            match[music_list[i]] = names[i]
    return match


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
