# Music

## Heart of Iron IV

- `find_all_music` function:This program will search music in 2 places: The `music` dir and `dlc` dir. For Stellaris it need to unzip `dlc*.zip`.(need `integrated_dlc`, Fuck Paradox add my code)It will search for the `.asset` file to get the music names and its file name.

- `find_music`: Find music in a dir.

- `get_music_names`:It will load the describe of the music from the localization file.

- `match_names`: Match music names with the given names.

- `copy_music`: Copy music to a dir.

- `read_asset`: Read the asset file to get music and its key.

### Source File

- localisation: "*_music_l_{lang}.yml"

- asset: "music*.asset"

- music path: "{game_path}/music", "{game_path}/dlc/{dlc_name}/music", "{game_path}/integrated_dlc/{dlc_name}/music"
