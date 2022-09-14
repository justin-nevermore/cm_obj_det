import time
import boto3
import tensorflow as tf
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector
assert tf.__version__.startswith('2')


begin = time.time()


def main(label, epoch_count=50, batch_size=4):

    train_data = object_detector.DataLoader.from_pascal_voc(
        images_dir='images/train',
        annotations_dir='images/train',
        label_map=[label]
    )

    val_data = object_detector.DataLoader.from_pascal_voc(
        images_dir='images/test',
        annotations_dir='images/test',
        label_map=[label]
    )

    spec = model_spec.get('efficientdet_lite0')

    model = object_detector.create(train_data, model_spec=spec, batch_size=batch_size, train_whole_model=True, epochs=epoch_count, validation_data=val_data)
    print('training Done')
    model.evaluate(val_data)
    print('Eval done')
    model.export(export_dir='/opt/amazon/', tflite_filename=f'{label}.tflite')
    print('Model saved')
    model.evaluate_tflite(f'/opt/amazon/{label}.tflite', val_data)
    print('model evaled')
    s3_client = boto3.client('s3')
    s3_client.upload_file(f'/opt/amazon/{label}.tflite', 'aws-cv-139243870339-trained-models', f'{label}.tflite')
    print('model uplaoded')
    end = time.time()
    print(f"Total runtime of the program is {(end - begin)/60} Min")
