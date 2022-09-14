import boto3

ecs_client = boto3.client('ecs', region_name='us-west-2')

def remove_spaces(custom_string):
    return custom_string.replace(' ', '_')


def create_ecs_tasks(label_name, epoch, output_path, batch_size, sample_count):
    response = ecs_client.run_task(
        cluster="arn:aws:ecs:us-west-2:139243870339:cluster/asset-id-generation",
        count=1,
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": [
                    "subnet-e25b17ca",
                    "subnet-e4cb8fbc",
                    "subnet-67978011",
                    "subnet-b6b549d1"
                ],
                "securityGroups": [
                    "sg-0fd7dc76",
                ],
                "assignPublicIp": "ENABLED",
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": f"model-trainer",
                    "environment": [
                        {
                            "name": "EPOCH",
                            "value": str(epoch)
                        },
                        {
                            "name": "LABEL",
                            "value": str(label_name)
                        },
                        {
                            "name": "OUTPUT_PATH",
                            "value": str(output_path)
                        },
                        {
                            "name": "BATCH_SIZE",
                            "value": str(batch_size)
                        },
                        {
                            "name": "SAMPLE_COUNT",
                            "value": str(sample_count)
                        },

                    ]
                },
            ],
            "executionRoleArn": "arn:aws:iam::139243870339:role/ecsTaskExecutionRole",
            "taskRoleArn": "arn:aws:iam::139243870339:role/ecsTaskExecutionRole",
        },
        taskDefinition="model-trainer:5",
    )

    print("Executing ECS Task: ", label_name)

    task_code = response["tasks"][0]["taskArn"].split("/")[-1]
    print("Task ID: {}".format(task_code))

data_dict = {
    # "Person": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/2020322-19202-Bboxdatadropsciencedataset2/",
    "Female Genitalia": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/202039-75325-Bboxscienceset2Cm/",
    "Male Genitalia": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/202039-75325-Bboxscienceset2Cm/",
    "Nude Female Breasts": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/202039-75325-Bboxscienceset2Cm/",
    # "Cleavage": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/202039-75325-Bboxscienceset2Cm/",
    "Sex Toys": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/2020322-19202-Bboxdatadropsciencedataset2/",
    "Nude Buttocks": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/2020322-19202-Bboxdatadropsciencedataset2/",
    "Male Barechest": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/2020322-19202-Bboxdatadropsciencedataset2/",
    # "Glasses": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Cigarettes": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    "Bottles": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Pills": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Mugs": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    "Bongs and Vaporizers": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Syringes": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Weed": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Joints": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    "Drug Powders": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    "Smoking Pipe": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "Hookah": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/",
    # "e-Cigarettes": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "KKK Symbol": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "Marijuana Leaf symbol": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "ISIS Flag": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "Nazi Swastika": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "Middle Finger": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "Pill Bottle": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    "Confederate Flag": "s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020410-101548-Datbboxcmbatch2/",
    # "Bulges": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/202052-73829-Bulgescmbbox02May2020/",
    # "Pokies": "s3://rekognition-content-moderation-annotations-shared/nudity/bbox/inhouse/202052-74830-Pokiescmbbox02May2020/"
}

for label_name, s3_path in data_dict.items():
    # fin_label_name = remove_spaces(label_name)
    create_ecs_tasks(label_name, 75, s3_path, 4, 750)