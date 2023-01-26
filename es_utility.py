import os, json, glob

def get_data(index, dir):
    content = []

    os.chdir(dir)
    
    for file in glob.glob('*.json'):
        f = open(file)
        data = json.load(f)

        for val in data.values():
            content.append({
                '_index': index,
                '_source': val
            })
        
    return content
