import setup_train_data
import trainer
import sys
import os

args = sys.argv
print(args)
output_path = args[1]
sample_count = int(args[2])
batch_size = int(args[3])
epoch = int(args[4])
label = ' '.join(args[5:])
current_dir = os.getcwd()
print('Started setting up training data')
setup_train_data.main(label, output_path, sample_count)
print('Completed setting up training data')
print('Started Training data')
trainer.main(label, epoch, batch_size)
print('Completed Training data')
