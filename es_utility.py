import os, json, glob

def get_data(index, dir):
    files = []

    os.chdir(dir)
    
    for file in glob.glob('*.json'):
        f = open(file)
        data = json.load(f)
        files.append({
            '_index': index,
            'data': data
        })

    return files