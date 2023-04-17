import torch
import os
import argparse


def create_parser():
    """Creates a parser for command-line arguments."""
    parser = argparse.ArgumentParser()

    # Model & Data hyper-parameters
    parser.add_argument("--task", type=str, default="", help="The task")

    # Training hyper-parameters
    parser.add_argument("--num_epochs", type=int, default=250)
    parser.add_argument(
        "--batch_size", type=int, default=16, help="The number of images in a batch"
    )

    parser.add_argument(
        "--num_workers",
        type=int,
        default=0,
        help="The number of threads to use for the DataLoader.",
    )

    parser.add_argument(
        "--lr", type=float, default=0.0001, help="The learning rate (default 0.0001)"
    )

    parser.add_argument(
        "--exp_name", type=str, default="exp", help="The name of the experiment"
    )

    # Directories and checkpoint/sample iterations
    parser.add_argument("--train_csv_path", type=str, default="../data/test.csv")
    parser.add_argument("--train_dataset_dir", type=str, default="../data/train")
    parser.add_argument("--test_dataset_dir", type=str, default="../data/test")
    parser.add_argument("--test_csv_path", type=str, default="../data/test.csv")
    parser.add_argument("--checkpoint_dir", type=str, default="../checkpoints")
    parser.add_argument("--checkpoint_every", type=int, default=10)
    parser.add_argument("--load_checkpoint", type=str, default="")
    parser.add_argument("--tensorboard_log_dir", type=str, default="../logs")

    return parser


def get_device():
    """
    Checks if GPU is available and returns device accordingly.
    """
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
    return device


def create_dir(directory):
    """
    Creates a directory if it does not already exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
