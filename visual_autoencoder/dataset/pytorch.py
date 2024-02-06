from torch.utils.data import Dataset
import torch
import numpy as np


class ImageDataset(Dataset):
    def __init__(self, images, transform=None):
        self.images = sum(images.values(),[])
        self.transform = transform
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image = self.images[idx]
        img = image.data
        if len(img.shape) == 3:
            # To grayscale
            img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])  # [:,:3] drop alpha
        img = img
        img = torch.from_numpy(img.astype(np.float32))
        if self.transform is not None:
            img = self.transform(img)
        return img

class collate_largest:
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def __call__(self, batch):
        shapes = torch.as_tensor([x.shape for x in batch])
        max_shape = torch.max(shapes, 0).values
        new_batch = torch.zeros((len(batch), 1, max_shape[0] // self.n * self.n + self.n, max_shape[1] // self.m * self.m + self.m))
        for i, x in enumerate(batch):
            new_batch[i, 0, :x.shape[0], :x.shape[1]] = x
        return new_batch