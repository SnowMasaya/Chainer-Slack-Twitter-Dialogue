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
from concurrent.futures import ProcessPoolExecutor, as_completed


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
    parser.add_argument('--set_worker', '-work', default=2,
                        help='set image Flag')
    args = parser.parse_args()
    Image_Flag = ast.literal_eval(args.img_flag)
    if Image_Flag is True:
        wikipedia_abstract_xml = APP_ROOT + "/../Data/wiki_image/" + args.xml_file
    else:
        wikipedia_abstract_xml = APP_ROOT + "/../Data/jawiki-20160901-abstract_dir/" + args.xml_file
    wiki_pedia_xml_to_json = WikiPediaXmlToJson(wikipedia_abstract_xml)
    wiki_pedia_xml_to_json.input(image_Flag=Image_Flag)

    # Multi Process
    with ProcessPoolExecutor() as executor:
        # executor.map(wiki_pedia_xml_to_json.extract_contents, wiki_pedia_xml_to_json.xml_data)
        all_process = []
        for xml_name in wiki_pedia_xml_to_json.xml_data:
            process = executor.submit(wiki_pedia_xml_to_json.extract_contents, xml_name)
            all_process.append(process)

        for process in as_completed(all_process):
            print(process.result())
