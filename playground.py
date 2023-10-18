import cv2
import torch
from PIL import Image
from torchvision import datasets, transforms
from torchvision.utils import save_image
import utils
import numpy as np

class DataAugmentationDINO_grayscale(object):
    def __init__(self, global_crops_scale, local_crops_scale, local_crops_number):
        flip_and_color_jitter = transforms.Compose([
            # transforms.Resize((480, 480)),resn
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomApply(
                [transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2, hue=0.1)],
                p=0.3
            ),
            # transforms.RandomGrayscale(p=0.2),
        ])
        normalize = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.485), (0.229)),
        ])

        # first global crop
        self.global_transfo1 = transforms.Compose([
            transforms.RandomResizedCrop(224, scale=global_crops_scale, interpolation=Image.BICUBIC),
            flip_and_color_jitter,
            utils.GaussianBlur(1.0),
            normalize,
        ])
        # second global crop
        self.global_transfo2 = transforms.Compose([
            transforms.RandomResizedCrop(224, scale=global_crops_scale, interpolation=Image.BICUBIC),
            flip_and_color_jitter,
            utils.GaussianBlur(0.1),
            utils.Solarization(0.2),
            normalize,
        ])
        # transformation for the local small crops
        self.local_crops_number = local_crops_number
        self.local_transfo = transforms.Compose([
            transforms.RandomResizedCrop(96, scale=local_crops_scale, interpolation=Image.BICUBIC),
            flip_and_color_jitter,
            utils.GaussianBlur(p=0.5),
            normalize,
        ])

    def __call__(self, image):
        crops = []
        crops.append(self.global_transfo1(image))
        crops.append(self.global_transfo2(image))
        for _ in range(self.local_crops_number):
            crops.append(self.local_transfo(image))
        return crops

def open_image(path):
    transform = DataAugmentationDINO_grayscale(
        (0.4, 1),
        (0.05, 0.4),
        8
    )

    pil_image_rgb = Image.open(path)
    pt = transform(pil_image_rgb)
    save_image(pt, "test_image/0.jpg")
    # print(pt)
    # print(pt.shape)

    # pil_image_l = pil_image_rgb.convert("L")

    # pil_tensor = transform(pil_image_l)
    # print(pil_tensor)
    # print(pil_tensor.shape)


    # image = cv2.imread(path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    # image_tensor = torch.from_numpy(image)
    # print(image_tensor)
    # print(image.shape)
    #
    # image_tensor_n = image_tensor/ 255.0
    # print(image_tensor_n)
    # print(image_tensor_n.shape)
                    # .unsqueeze(dim=0))

    # return image_tensor

if __name__ == "__main__":
    open_image("dataset/train/1/0.jpg")
    open_image("dataset/train/1/96.jpg")
    open_image("dataset/train/1/154.jpg")
    open_image("dataset/train/1/203.jpg")
    open_image("dataset/train/1/281.jpg")
