import os
import glob
import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_csv(path):
    classes_names = []
    xml_list = []

    for xml_file in glob.glob(os.path.join(path, '*.xml')):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        filename = root.find('filename').text
        width = int(root.find('size').find('width').text)
        height = int(root.find('size').find('height').text)

        for member in root.findall('object'):
            class_name = member.find('name').text
            xmin = int(member.find('bndbox').find('xmin').text)
            ymin = int(member.find('bndbox').find('ymin').text)
            xmax = int(member.find('bndbox').find('xmax').text)
            ymax = int(member.find('bndbox').find('ymax').text)

            classes_names.append(class_name)
            value = (filename, width, height, class_name, xmin, ymin, xmax, ymax)
            xml_list.append(value)

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)

    classes_names = list(set(classes_names))
    classes_names.sort()

    return xml_df, classes_names

if __name__ == "__main__":
    data_dir = "/mydrive/customTF2/data/"
    
    for label_path in ['train_labels', 'test_labels']:
        image_path = os.path.join(os.getcwd(), label_path)
        xml_df, classes = xml_to_csv(os.path.join(data_dir, label_path))
        xml_df.to_csv(os.path.join(data_dir, f'{label_path}.csv'), index=None)
        print(f'Successfully converted {label_path} xml to csv.')

    label_map_path = os.path.join(data_dir, "label_map.pbtxt")
    pbtxt_content = ""

    for i, class_name in enumerate(classes):
        pbtxt_content += "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(i + 1, class_name)

    pbtxt_content = pbtxt_content.strip()

    with open(label_map_path, "w") as f:
        f.write(pbtxt_content)
        print('Successfully created label_map.pbtxt')
