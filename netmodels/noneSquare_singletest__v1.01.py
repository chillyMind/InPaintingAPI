from __future__ import print_function
import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
from torch.autograd import Variable

from modelAlpha import _netWG

import utils


parser = argparse.ArgumentParser()
parser.add_argument('--dataset',  default='streetview', help='cifar10 | lsun | imagenet | folder | lfw ')
parser.add_argument('--testimg', required=True, help='path to dataset')
parser.add_argument('--workers', type=int, help='number of data loading workers', default=2)
parser.add_argument('--batchSize', type=int, default=64, help='input batch size')
parser.add_argument('--imageSize', type=int, default=128, help='the height / width of the input image to network')
parser.add_argument('--nz', type=int, default=100, help='size of the latent z vector')
parser.add_argument('--ngf', type=int, default=128)
parser.add_argument('--ndf', type=int, default=128)
parser.add_argument('--nc', type=int, default=4)
parser.add_argument('--niter', type=int, default=1, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.0002, help='learning rate, default=0.0002')
parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. default=0.5')
parser.add_argument('--cuda', default=True, help='enables cuda')
parser.add_argument('--ngpu', type=int, default=1, help='number of GPUs to use')
parser.add_argument('--netG', default='netmodels/model/netG_streetview_0.pth', help="path to netG (to continue training)")
parser.add_argument('--outf', default='.', help='folder to output images and model checkpoints')
parser.add_argument('--manualSeed', type=int, help='manual seed')

parser.add_argument('--nBottleneck', type=int,default=4000,help='of dim for bottleneck of encoder')
parser.add_argument('--overlapPred',type=int,default=0,help='overlapping edges')
parser.add_argument('--nef',type=int,default=64,help='of encoder filters in first conv layer')
parser.add_argument('--wtl2',type=float,default=0.999,help='0 means do not use else use with this weight')
opt = parser.parse_args()
print(opt)

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


netG = _netWG(opt)
netG.apply(weights_init)
netG.load_state_dict(torch.load(opt.netG,map_location=lambda storage, location: storage)['state_dict'])
resume_epoch = torch.load(opt.netG)['epoch']
netG.eval()
print(netG)

#image_margin = int((opt.imageSize - opt.ndf)/2)
image_margin = 0
transform = transforms.Compose([transforms.ToTensor()])

png_image = utils.load_image(opt.testimg, opt.imageSize)
png_image = transform(png_image)
input_cropped = torch.FloatTensor(1, 4, opt.imageSize, opt.imageSize)
input_pngReverse = torch.FloatTensor(4, opt.ndf, opt.ndf)
result_img = torch.FloatTensor(1, 3, opt.imageSize, opt.imageSize)
input_cropped = Variable(input_cropped)



#input_cropped.data.resize_(png_image.size()).copy_(png_image)
input_pngReverse[0] = png_image[3][image_margin:image_margin+opt.ndf, image_margin:image_margin+opt.ndf]
png_imageV = Variable(png_image)
input_cropped.data[0,0] = png_imageV.data[0]
input_cropped.data[0,1] = png_imageV.data[1]
input_cropped.data[0,2] = png_imageV.data[2]
input_cropped.data[0,0,
                  image_margin:image_margin+opt.ndf,
                  image_margin:image_margin+opt.ndf] = input_pngReverse[0] * input_cropped.data[0,0,
                  image_margin:image_margin+opt.ndf,
                  image_margin:image_margin+opt.ndf]
input_cropped.data[0,1,
                  image_margin:image_margin+opt.ndf,
                  image_margin:image_margin+opt.ndf] = input_pngReverse[0] * input_cropped.data[0,1,
                  image_margin:image_margin+opt.ndf,
                  image_margin:image_margin+opt.ndf]
input_cropped.data[0,2,
                  image_margin:image_margin+opt.ndf,
                  image_margin:image_margin+opt.ndf] = input_pngReverse[0] * input_cropped.data[0,2,
                  image_margin:image_margin+opt.ndf,
                  image_margin:image_margin+opt.ndf]
input_cropped.data[0,3] = png_image[3]
input_pngReverse[0] = torch.abs(png_image[3] - 1)[image_margin:image_margin+opt.ndf, image_margin:image_margin+opt.ndf]

epoch = resume_epoch

# train with fake
fake = netG(input_cropped)

result_img[0,0] = input_cropped.data[0,0]
result_img[0,1] = input_cropped.data[0,1]
result_img[0,2] = input_cropped.data[0,2]
vutils.save_image(result_img[0],'public/result/%s.png' % (opt.testimg))
result_img[0,0,
     image_margin:image_margin+opt.ndf,
     image_margin:image_margin+opt.ndf] += fake.data[0,0] * input_pngReverse[0]
result_img[0,1,
     image_margin:image_margin+opt.ndf,
     image_margin:image_margin+opt.ndf] += fake.data[0,1] * input_pngReverse[0]
result_img[0,2,
     image_margin:image_margin+opt.ndf,
     image_margin:image_margin+opt.ndf] += fake.data[0,2] * input_pngReverse[0]
vutils.save_image(result_img[0],'public/result/%s.png' % (opt.testimg))
result_img[0,0] = input_cropped.data[0,0]
result_img[0,1] = input_cropped.data[0,1]
result_img[0,2] = input_cropped.data[0,2]
result_img[0,0,
     image_margin:image_margin+opt.ndf,
     image_margin:image_margin+opt.ndf] = fake.data[0,0]
result_img[0,1,
     image_margin:image_margin+opt.ndf,
     image_margin:image_margin+opt.ndf] = fake.data[0,1]
result_img[0,2,
     image_margin:image_margin+opt.ndf,
     image_margin:image_margin+opt.ndf] = fake.data[0,2]

vutils.save_image(result_img[0],'public/result/%s.png' % (opt.testimg))
