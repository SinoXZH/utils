#coding:utf-8
'''
Author: xuziheng
Date: 2020/02/06
description:
sometimes softlink files of linux cannot be recognized.
use this script to copy the real file to the link files.
put the script in the root directory and run.
dependency: python 2.7
'''

import os

def split_path(file_path):
    path_list = file_path.split('/')
    file_name = path_list[len(path_list) - 1]
    dir_name = file_path.replace('/' + file_name, '')
    return dir_name, file_name

def get_link_target(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) != 1:
            return None
        content = lines[0]
        content = content.strip()
        if len(content) > 128 or len(content) == 0:
            return None
        
        dir_name, file_name = split_path(file_path)
        link_path = os.path.join(dir_name, content)
        if os.path.isfile(link_path):
            return link_path
        return None


def process_file(file_path):
    #print 'INFO: processing {}'.format(file_path)
    link_path_list = []
    real_file = ''
    while True:
        link_path = get_link_target(file_path)
        if link_path == None:
            real_file = file_path
            break
        else:
            link_path_list.append(file_path)
            file_path = link_path

    for link_path in link_path_list:
        print 'actualize link file {} to real file {}'.format(link_path, real_file)
        os.system('cp {} {}'.format(real_file, link_path))


def recursive_dir(cur_dir):
    if not os.path.isdir(cur_dir):
        return
    
    sub_name_list = os.listdir(cur_dir)
    for sub_name in sub_name_list:
        sub_path = os.path.join(cur_dir, sub_name)
        if os.path.isdir(sub_path):
            recursive_dir(sub_path)
        elif os.path.isfile(sub_path):
            process_file(sub_path)
        else:
            print 'WARNING: invalid path: {}'.format(sub_path)


def main():
    recursive_dir(os.getcwd())


if __name__ == '__main__':
    main()