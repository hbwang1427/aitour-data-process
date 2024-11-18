import os, sys
import json
import filecmp

if __name__ == '__main__':
    ann_file1 = sys.argv[1]
    ann_file2 = sys.argv[2]

    ann1 = json.load(open(ann_file1, 'r'))
    ann2 = json.load(open(ann_file2, 'r'))

    all_files = list(set(ann1.keys() + ann2.keys()))
    print len(ann1), len(ann2), len(all_files)
    results = {}
    for item in all_files:
        list1 = ann1[item] if item in ann1 else []
        list2 = ann2[item] if item in ann2 else []
        combined_list = list(set(list1 + list2))
        if len(combined_list) > 0:
            results[item] = combined_list
            print item
        #print item, len(results[item])

#    for i in range(len(all_files)):
#       print all_files[i]
#        for j in range(i+1, len(all_files)):
#            if filecmp.cmp(all_files[i].replace('_small', ''), all_files[j].replace('_small', '')):
#                print all_files[i], all_files[j]

    print len(results)
    json.dump(results, open('annotations/mfa_annotation.json', 'w'))
    
