#!/usr/bin/env python
#coding: utf8
import sys
import os
from os import path
sys.path.append(os.path.join(os.path.dirname("__file__"), "./../"))
sys.path.append(os.path.join(os.path.dirname("__file__"), "."))
APP_ROOT = path.dirname(path.abspath(__file__))
import ast
from wiki_pedia_xml_to_json import WikiPediaXmlToJson
import argparse

if __name__ == '__main__':
    """
    Reference (str to boolean)
        http://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
    args
    --xml_file: set the xml file
        Example: APP_ROOT + "/../Data/jawiki-20160901-abstract.xml"
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_file', '-xml', default='jawiki-20160901-abstract_part.xml',
                        help='set xml file')
    parser.add_argument('--img_flag', '-img', default="False",
                        help='set image Flag')
    args = parser.parse_args()
    wikipedia_abstract_xml = APP_ROOT + "/../Data/jawiki-20160901-abstract_dir/" + args.xml_file
    wiki_pedia_xml_to_json = WikiPediaXmlToJson(wikipedia_abstract_xml)
    wiki_pedia_xml_to_json.input(image_Flag=ast.literal_eval(args.img))
