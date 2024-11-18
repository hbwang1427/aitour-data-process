import os, sys
import json
import filecmp
    
def convert_annotations(data):
    annotation = list()
    for key, value in data.items():
        if value:
            x = set(value)
            x.add(key)
            annotation.append(x)

    for k1 in range(len(annotation)):
        for k2 in range(k1+1,len(annotation)):
           if annotation[k1].intersection(annotation[k2]):
               annotation[k1].union(annotation[k2])
               annotation[k2] = set()
    return annotation

if __name__ == '__main__':
    annotation_basedir = '/home/pangolins/work/data/annotations'
    dataset = sys.argv[1]
    ann_file1 = os.path.join(annotation_basedir, dataset, dataset+'_annotation.json')
    ann_file2 = os.path.join(annotation_basedir, dataset, dataset+'_annotation.txt')
    if os.path.isfile(ann_file2):
       for k in range(1, 10):
           backup_file = os.path.join(annotation_basedir, dataset, dataset+'_annotation.txt-save%d' %(k))
           if not os.path.isfile(backup_file):
               break
       os.rename(ann_file2, backup_file)

    json_data = json.load(open(ann_file1, 'r'))
    annotation = convert_annotations(json_data) 
        
    ann_str = [','.join(item) for item in annotation if len(item) > 0]

    ann_file = os.path.join(ann_file2)
    with open(ann_file, 'wt') as fid:
        for item in ann_str:
            fid.write(item+'\r\n')
