import torch
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

from utils import get_device, create_dir, create_parser
from nlos_dataset import NLOSDataset


def train(args, train_dataloader, model, optimizer, epoch, tensorboard_writer):
    model.train()
    step = epoch * len(train_dataloader)
    criterion = torch.nn.CrossEntropyLoss(reduction="mean")

    for index, batch in enumerate(train_dataloader):
        scattering_images, gt_images = batch
        scattering_images = scattering_images.to(args.device)
        gt_images = gt_images.to(args.device)

        predicted_images = model.forward(scattering_images)

        # Compute loss
        loss = criterion(predicted_images, gt_images)
        epoch_loss += loss

        # backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        tensorboard_writer.add_scalar("train_loss", loss.item(), step + index)

    return epoch_loss


def train(args, test_dataloader, model, epoch, tensorboard_writer):
    model.eval()
    for batch in test_dataloader:
        scattering_images, gt_images = batch
        scattering_images = scattering_images.to(args.device)
        gt_images = gt_images.to(args.device)

        with torch.no_grad():
            predicted_images = model.forward(scattering_images)

        


def main(args):
    # create tensorboard folder
    create_dir(args.tensorboard_log_dir)

    # initialize tensorboard writer
    tensorboard_writer = SummaryWriter(log_dir=args.tensorboard_log_dir)

    # initialize model
    model = torch.hub.load(
        "mateuszbuda/brain-segmentation-pytorch",
        "unet",
        in_channels=1,
        out_channels=1,
        init_features=32,
        pretrained=False,
    )
    model = model.to(args.device)

    # setup optimizer
    optimizer = optim.Adam(model.parameters(), args.lr, betas=(0.9, 0.999))

    # Dataloader for Training & Testing
    train_dataloader = NLOSDataset.get_data_loader(args=args, train=True)
    test_dataloader = NLOSDataset.get_data_loader(args=args, train=False)

    for epoch in range(args.num_epochs):
        train_epoch_loss = train(
            args, train_dataloader, model, optimizer, epoch, tensorboard_writer
        )

        # Test
        current_acc = test(test_dataloader, model, epoch, args, writer)


if __name__ == "__main__":
    paser = create_parser()
    args = paser.parse_args()
    args.device = get_device()

    main(args)
