import setup_train_data
import trainer
import sys
import os


args = sys.argv
print(args)
output_path = "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/"  # args[1]  # 
sample_count = 300  # int(args[2])  # 
label = "Joints"  # args[3]  # 
batch_size = 4  # int(args[4])  #  
epoch = 10  # int(args[5])  # 
current_dir = os.getcwd()
print(current_dir)
print('Started setting up training data')
setup_train_data.main(label, output_path, sample_count)
print('Completed setting up training data')
print('Started Training data')
trainer.main(label, epoch, batch_size)
print('Completed Training data')
# except Exception as e:
    # print('Exception occured : ', e)