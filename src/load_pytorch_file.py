import torch
import sys

torch_file=sys.argv[1]
weight=torch.load(torch_file)

print(weight.shape)

