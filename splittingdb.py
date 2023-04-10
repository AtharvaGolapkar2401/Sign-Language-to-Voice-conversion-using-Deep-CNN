import splitfolders

input_folder = 'data2/'

splitfolders.ratio(input_folder, output='dataset2', seed=42, ratio=(.7, .2, .1), group_prefix=None)

splitfolders.fixed(input_folder, output='dataset2', seed=42, fixed=(200, 200), oversample=False, group_prefix=None)