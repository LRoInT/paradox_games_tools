# Can use for all games

import os


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

def match_names(music_list, names):
    match = {}
    for i in music_list:
            match[music_list[i]] = names[i] if i in names else "Unknown"
    return match

def find_music(music_path):
    # 在目录中查找所有音乐文件 Find all music files in a directory
    music_list = {}
    for f in os.listdir(music_path):
        if f.endswith(".asset") and "music" in f:
            music_list.update(read_asset(os.path.join(music_path, f)))
        elif os.path.isdir(p := os.path.join(music_path, f)):
            music_list.update(find_music(p))
    return music_list

