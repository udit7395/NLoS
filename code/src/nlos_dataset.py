import pathlib
import PIL
import pandas as pd

import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader


class NLOSDataset(Dataset):
    def __init__(self, path_to_csv, path_to_dataset, transforms):
        self.csv_pd_file = pd.read_csv(str(path_to_csv), sep=",")
        self.transform = transforms
        self.path_to_dataset = path_to_dataset

    def __len__(self):
        return self.csv_pd_file.shape[0]  # get number of rows

    def __getitem__(self, index):
        scattering_image = self.get_image(index, column_name="scattering_image_path")
        ground_truth_image = self.get_image(
            index, column_name="ground_truth_image_path"
        )
        return scattering_image, ground_truth_image

    @classmethod
    def get_image(self, index, column_name):
        image_path = self.path_to_dataset / self.csv_pd_file[index][column_name]
        image = PIL.Image.open(str(image_path))
        transformed_image = self.transform(image)
        return transformed_image

    @staticmethod
    def get_transform_for_unet(self, resize_image=256):
        # TODO Confirm if normalization is required?
        transform_for_unet = transforms.Compose(
            [
                transforms.Grayscale(),
                transforms.Resize(
                    size=(resize_image, resize_image),
                    interpolation=transforms.functional.InterpolationMode.BICUBIC,
                ),
                transforms.ToTensor(),
                # transforms.Normalize(mean = (0.1307,), std = (0.3081,)) #https://stackoverflow.com/questions/63746182/correct-way-of-normalizing-and-scaling-the-mnist-dataset
            ]
        )
        return transform_for_unet

    @staticmethod
    def get_data_loader(args, train):
        """
        Creates training and test data loaders
        """

        if train:
            dataset = NLOSDataset(
                path_to_csv=args.train_csv_path,
                path_to_dataset=args.train_dataset_dir,
                transforms=NLOSDataset.get_transform_for_unet(),
            )

            data_loader = DataLoader(
                dataset=dataset,
                batch_size=args.batch_size,
                shuffle=True,
                num_workers=args.num_workers,
            )
        else:
            dataset = NLOSDataset(
                path_to_csv=args.test_csv_path,
                path_to_dataset=args.test_dataset_dir,
                transforms=NLOSDataset.get_transform_for_unet(),
            )

            data_loader = DataLoader(
                dataset=dataset,
                batch_size=args.batch_size,
                shuffle=True,
                num_workers=args.num_workers,
            )
        return data_loader


if __name__ == "__main__":
    train_path_to_csv = pathlib.Path("").absolute()
    train_path_to_dataset = pathlib.Path("").absolute()
    train_nlos_dataset = NLOSDataset(
        path_to_csv=train_path_to_csv,
        path_to_dataset=train_path_to_dataset,
        transforms=NLOSDataset.get_transform_for_unet(),
    )

    test_path_to_csv = pathlib.Path("").absolute()
    test_path_to_dataset = pathlib.Path("").absolute()
    test_nlos_dataset = NLOSDataset(
        path_to_csv=test_path_to_csv,
        path_to_dataset=test_path_to_dataset,
        transforms=NLOSDataset.get_transform_for_unet(),
    )

    index = 0
    scattering_image, ground_truth_image = train_nlos_dataset[index]

    figure = plt.figure(figsize=(8, 8))

    figure.add_subplot(0, 0, 0)
    plt.title(f"train_dataset_scattering_image_{index}")
    plt.imshow(scattering_image.squeeze(0))
    plt.axis("off")

    figure.add_subplot(0, 1, 1)
    plt.title(f"train_dataset_gt_image_{index}")
    plt.imshow(ground_truth_image.squeeze(0))
    plt.axis("off")

    scattering_image, ground_truth_image = test_nlos_dataset[index]

    figure.add_subplot(1, 0, 0)
    plt.title(f"test_dataset_scattering_image_{index}")
    plt.imshow(scattering_image.squeeze(0))
    plt.axis("off")

    figure.add_subplot(1, 1, 1)
    plt.title(f"test_dataset_gt_image_{index}")
    plt.imshow(ground_truth_image.squeeze(0))
    plt.axis("off")

    plt.show()
