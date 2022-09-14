from multiprocessing.dummy import Value
import json
import glob
import boto3
import os
import shutil
import numpy as np
from PIL import Image
from xml.dom import minidom
import xml.etree.ElementTree as etree  # import Element, SubElement, tostring
s3 = boto3.resource("s3")
# file_object = s3.Object("jusjar-cm", f'py_files/create_pascal_tfrecord.py')
# with open("/usr/local/lib/python3.7/site-packages/tensorflow_examples/lite/model_maker/third_party/efficientdet/dataset/create_pascal_tfrecord.py", 'r') as f:
#     file_data = f.read()
#     file_object.put(Body=file_data)

if not os.path.exists('images'):
    os.mkdir('images')

def read_image_as_array_from_s3(bucket, key):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return im


def extract_labels(label, json_data):
    for label_id, label_data in json_data.items():
        if ' - BBox' in label_data['Name']:
            if label_data['Name'][:-10] == label:
                return label_id
        else:
            if label_data['Name'][:-5] == label:
                return label_id
    return False
    

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = etree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def convert_annotations(annotations_data, label, folder_name, label_id):
    for image_uri, annotations in annotations_data.items():
        xml_head = etree.Element('annotation')
        src = etree.SubElement(xml_head, 'source')
        etree.SubElement(src, 'database').text = 'Unknown'
        filename = os.path.basename(image_uri)
        etree.SubElement(xml_head, 'filename').text = filename
        etree.SubElement(xml_head, 'folder').text = f"images/{folder_name}"
        etree.SubElement(xml_head, 'segmented').text = "0"
        size = etree.SubElement(xml_head, 'size')
        etree.SubElement(size, 'height').text = str(annotations['size']['height'])
        etree.SubElement(size, 'width').text = str(annotations['size']['width'])
        etree.SubElement(size, 'depth').text = str(annotations['size']['depth'])
        for index, annotation in enumerate(annotations['annotations']):
            if index < 25:
                bbx_object = etree.SubElement(xml_head, 'object')
                etree.SubElement(bbx_object, 'name').text = label
                etree.SubElement(bbx_object, 'pose').text = 'Unspecified'
                etree.SubElement(bbx_object, 'truncated').text = "0"
                etree.SubElement(bbx_object, 'difficult').text = "0"
                bndbox = etree.SubElement(bbx_object, 'bndbox')
                xmin = etree.SubElement(bndbox, 'xmin')
                xmin.text = str(annotation['xmin'])
                ymin = etree.SubElement(bndbox, 'ymin')
                ymin.text = str(annotation['ymin'])
                xmax = etree.SubElement(bndbox, 'xmax')
                xmax.text = str(annotation['xmax'])
                ymax = etree.SubElement(bndbox, 'ymax')
                ymax.text = str(annotation['ymax'])
            else:
                break
        with open(f'images/{folder_name}/{filename}.xml', 'w') as f:
            f.write(prettify(xml_head))
        file_object = s3.Object("jusjar-cm", f'images/{folder_name}/{filename}.xml')
        file_object.put(Body=prettify(xml_head))


def get_s3_json_data(bucket, prefix_path):
    file_obj = s3.Object(bucket, prefix_path)
    json_object = json.loads(file_obj.get()['Body'].read().decode())
    return json_object


def main(given_label, output_path, limit=1000):
    s3_uri = output_path
    bucket, key = s3_uri[5:].split('/', 1)
    asset_uri = key + 'assets.json'
    annotations_uri = key + 'annotations.json'
    labels_uri = key + 'labels.json'

    annotations_data = get_s3_json_data(bucket, annotations_uri)
    labels_data = get_s3_json_data(bucket, labels_uri)
    asset_data = get_s3_json_data(bucket, asset_uri)

    all_annotation_data = {}
    count = 0
    breaker = False
    label_id = extract_labels(given_label, labels_data)
    for asset_id, ann_data in annotations_data[label_id].items():
        if breaker:
            break
        asset_uri = f"s3://{asset_data[asset_id]['S3Bucket']}/{asset_data[asset_id]['S3Key']}"
        img = read_image_as_array_from_s3(asset_data[asset_id]['S3Bucket'], asset_data[asset_id]['S3Key'])
        img_format = img.format
        if img_format.lower() not in ['jpg', 'jpeg', 'png']:
            print("skipping image since format is : ", img_format)
            continue
        try:
            height, width, depth = np.asarray(img).shape
        except ValueError:
            height, width = np.asarray(img).shape
            depth = 1
        if asset_uri not in all_annotation_data:
            all_annotation_data[asset_uri] = {
                "size": {
                    "height": height,
                    "width": width,
                    "depth": depth
                    }, 
                "annotations": []
                }
            filename = os.path.basename(asset_uri)
            img.save(f"images/{filename}")
        for _, annotations in ann_data.items():
            for annotation in annotations:
                xmin = annotation['X'] * width
                ymin = annotation['Y'] * height
                xmax = annotation['W'] * width
                ymax = annotation['H'] * height
                label = labels_data[annotation['LabelId']]['Name']
                if float(str(xmin).split('.')[0] + '.' + str(xmin).split('.')[-1][:3]) == 69.383:
                    a = 23
                all_annotation_data[asset_uri]["annotations"].append({
                    "xmin": float(str(xmin).split('.')[0] + '.' + str(xmin).split('.')[-1][:3]),
                    "ymin": float(str(ymin).split('.')[0] + '.' + str(ymin).split('.')[-1][:3]),
                    "xmax": float(str(xmax).split('.')[0] + '.' + str(xmax).split('.')[-1][:3]),
                    "ymax": float(str(ymax).split('.')[0] + '.' + str(ymax).split('.')[-1][:3]),
                    # "xmin": int(str(xmin)),
                    # "ymin": int(str(ymin)),
                    # "xmax": int(str(xmax)),
                    # "ymax": int(str(ymax)),
                    "label": label
                })
        count += 1
        if count == limit:
            breaker = True
            break

    train_count = int(0.8 * count)

    image_list = glob.glob('images/*')
    train_list = image_list[:train_count]
    train_image_list = [os.path.basename(image_path) for image_path in train_list]
    test_list = image_list[train_count:]
    print(glob.glob(os.getcwd() + '/*'))

    os.mkdir('images/test')
    for file in test_list:
        shutil.move(file, f"images/test/{file.split('/')[-1]}")
    os.mkdir('images/train')
    for file in train_list:
        shutil.move(file, f"images/train/{file.split('/')[-1]}")

    training_annotation_data = {}
    testing_annotation_data = {}
    for image_uri, data in all_annotation_data.items():
        image_name = os.path.basename(image_uri)
        if "images/" + image_name in train_list:
            training_annotation_data[image_uri] = data
        else:
            testing_annotation_data[image_uri] = data

    convert_annotations(annotations_data=training_annotation_data, label=given_label, folder_name='train', label_id=label_id)
    convert_annotations(annotations_data=testing_annotation_data, label=given_label, folder_name='test', label_id=label_id)
