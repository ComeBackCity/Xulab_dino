import shutil
import os
from tqdm import tqdm

if __name__ == "__main__":

    train_ann_dir = "dataset_ramisa/annotation_train"
    test_ann_dir = "dataset_ramisa/annotation_test"
    train_set_dir = "dataset_ramisa/train/1"
    test_set_dir = "dataset_ramisa/test/1"

    new_train_ann_dir = "dataset_new/annotation_train"
    new_test_ann_dir = "dataset_new/annotation_test"
    new_train_set_dir = "dataset_new/train/1"
    new_test_set_dir = "dataset_new/test/1"

    train_anns = os.listdir(train_ann_dir)
    test_anns = os.listdir(test_ann_dir)

    for train_ann in train_anns:
        image_path = f"{train_ann[:-4]}.jpg"
        shutil.copy(
            os.path.join(train_ann_dir, train_ann),
            os.path.join(new_train_ann_dir)
        )

        shutil.copy(
            os.path.join(train_set_dir, image_path),
            os.path.join(new_train_set_dir)
        )

    for test_ann in (test_anns):
        image_path = f"{test_ann[:-4]}.jpg"
        shutil.copy(
            os.path.join(test_ann_dir, test_ann),
            os.path.join(new_test_ann_dir)
        )

        shutil.copy(
            os.path.join(test_set_dir, image_path),
            os.path.join(new_test_set_dir)
        )