import os, json, glob, random

def get_data(index, dir):
    content = []
    limit = 1

    os.chdir(dir)
    files = glob.glob('*.json')
    random.shuffle(files)
    
    i = 0
    for file in glob.glob('*.json'):
        if i >= limit:
            break
        i += 1

        f = open(file)
        data = json.load(f)

        for val in data.values():
            val['likes'] = random.randint(0, 10)
            content.append({
                '_index': index,
                '_source': val,
            })
    return content
