# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.utils as tutils
from torch.autograd import Variable
from torch.utils.data.sampler import SubsetRandomSampler
import matplotlib.pyplot as plt
# import sklearn.metrics as sm
# import pandas as pd
# import sklearn.metrics as sm
import random
import numpy as np

# from wideresnet import WideResNet, VNet
from resnet import ResNet32,VNet
from resnet_basic import ResNet32_Basic
from load_corrupted_data import CIFAR10, CIFAR100

# to visualize
from torch.utils.tensorboard import SummaryWriter

parser = argparse.ArgumentParser(description='PyTorch WideResNet Training')
parser.add_argument('--dataset', default='cifar10', type=str,
                    help='dataset (cifar10 [default] or cifar100)')

# corruption level and type
parser.add_argument('--corruption_prob_meta', type=float, default=0.4,
                    help='meta label noise')
parser.add_argument('--corruption_prob_train', type=float, default=0.4,
                    help='train label noise')
parser.add_argument('--corruption_type_meta', type=str, default='unif',
                    help='Type of meta corruption ("unif" or "flip" or "flip2").')
parser.add_argument('--corruption_type_train', '-ctype', type=str, default='unif',
                    help='Type of train corruption ("unif" or "flip" or "flip2").')

# LNL or not
parser.add_argument('--LNL', type=bool, default=False,
                    help='LNL or not')

parser.add_argument('--num_meta', type=int, default=1000)
parser.add_argument('--epochs', default=120, type=int,
                    help='number of total epochs to run')
parser.add_argument('--iters', default=60000, type=int,
                    help='number of total iters to run')
parser.add_argument('--start-epoch', default=0, type=int,
                    help='manual epoch number (useful on restarts)')
parser.add_argument('--batch_size', '--batch-size', default=100, type=int,
                    help='mini-batch size (default: 100)')
parser.add_argument('--lr', '--learning-rate', default=1e-1, type=float,
                    help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
parser.add_argument('--nesterov', default=True, type=bool, help='nesterov momentum')
parser.add_argument('--weight-decay', '--wd', default=5e-4, type=float,
                    help='weight decay (default: 5e-4)')
parser.add_argument('--print-freq', '-p', default=10, type=int,
                    help='print frequency (default: 10)')
parser.add_argument('--layers', default=28, type=int,
                    help='total number of layers (default: 28)')
parser.add_argument('--widen-factor', default=10, type=int,
                    help='widen factor (default: 10)')
parser.add_argument('--droprate', default=0, type=float,
                    help='dropout probability (default: 0.0)')
parser.add_argument('--no-augment', dest='augment', action='store_false',
                    help='whether to use standard augmentation (default: True)')
parser.add_argument('--resume', default='', type=str,
                    help='path to latest checkpoint (default: none)')
parser.add_argument('--name', default='WideResNet-28-10', type=str,
                    help='name of experiment')
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--prefetch', type=int, default=0, help='Pre-fetching threads.')
parser.set_defaults(augment=True)

args = parser.parse_args()
use_cuda = True
torch.manual_seed(args.seed)
device = torch.device("cuda" if use_cuda else "cpu")


print()
print(args)

m_type = args.corruption_type_meta
t_type = args.corruption_type_train
m_rate = str(args.corruption_prob_meta)
t_rate = str(args.corruption_prob_train)
print(m_type, t_type, m_rate, t_rate)


infoname = m_type + m_rate+ t_type + t_rate + time.strftime("%Y%m%d-%H%M%S")
pathname= args.dataset + "/" + infoname
writer = SummaryWriter('runs/' + pathname)


def build_dataset():
    normalize = transforms.Normalize(mean=[x / 255.0 for x in [125.3, 123.0, 113.9]],
                                     std=[x / 255.0 for x in [63.0, 62.1, 66.7]])
    if args.augment:
        train_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: F.pad(x.unsqueeze(0),
                                              (4, 4, 4, 4), mode='reflect').squeeze()),
            transforms.ToPILImage(),
            transforms.RandomCrop(32),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ])
    else:
        train_transform = transforms.Compose([
            transforms.ToTensor(),
            normalize,
        ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        normalize
    ])

    if args.dataset == 'cifar10':
        train_data_meta = CIFAR10(
            root='../data', train=True, meta=True, num_meta=args.num_meta,
            corruption_prob_meta=args.corruption_prob_meta, corruption_prob_train=args.corruption_prob_train,
            corruption_type_meta=args.corruption_type_meta, corruption_type_train=args.corruption_type_train, 
            transform=train_transform, download=True)
        train_data = CIFAR10(
            root='../data', train=True, meta=False, num_meta=args.num_meta,
            corruption_prob_meta=args.corruption_prob_meta, corruption_prob_train=args.corruption_prob_train,
            corruption_type_meta=args.corruption_type_meta, corruption_type_train=args.corruption_type_train, 
            transform=train_transform, download=True, seed=args.seed)
        test_data = CIFAR10(root='../data', train=False, transform=test_transform, download=True)


    elif args.dataset == 'cifar100':
        train_data_meta = CIFAR100(
            root='../data', train=True, meta=True, num_meta=args.num_meta,
            corruption_prob_meta=args.corruption_prob_meta, corruption_prob_train=args.corruption_prob_train,
            corruption_type_meta=args.corruption_type_meta, corruption_type_train=args.corruption_type_train, 
            transform=train_transform, download=True)
        train_data = CIFAR100(
            root='../data', train=True, meta=False, num_meta=args.num_meta,
            corruption_prob_meta=args.corruption_prob_meta, corruption_prob_train=args.corruption_prob_train,
            corruption_type_meta=args.corruption_type_meta, corruption_type_train=args.corruption_type_train, 
            transform=train_transform, download=True, seed=args.seed)
        test_data = CIFAR100(root='../data', train=False, transform=test_transform, download=True)

    train_loader = torch.utils.data.DataLoader(
        train_data, batch_size=args.batch_size, shuffle=True,
        num_workers=args.prefetch, pin_memory=True)
    train_meta_loader = torch.utils.data.DataLoader(
        train_data_meta, batch_size=args.batch_size, shuffle=True,
        num_workers=args.prefetch, pin_memory=True)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=args.batch_size, shuffle=False,
                                              num_workers=args.prefetch, pin_memory=True)
    
    return train_loader, train_meta_loader, test_loader


def build_model():
    if args.LNL == False:
        # load ResNet32 basic model (not mwnet)
        print("BASIC MODEL CALLED by build_model")
        model = ResNet32_Basic(args.dataset == 'cifar10' and 10 or 100)
    else:
        model = ResNet32(args.dataset == 'cifar10' and 10 or 100)

    if torch.cuda.is_available():
        model.cuda()
        torch.backends.cudnn.benchmark = True

    return model

def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


def adjust_learning_rate(optimizer, epochs):
    lr = args.lr * ((0.1 ** int(epochs >= 80)) * (0.1 ** int(epochs >= 100)))  # For WRN-28-10
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


# accuracy measured on test data
def test(model, vnet, test_loader, epoch):
    model.eval()
    correct = 0
    test_loss = 0

    with torch.no_grad():
        for batch_idx, (inputs, targets) in enumerate(test_loader):
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            test_loss +=F.cross_entropy(outputs, targets).item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()

    test_loss /= len(test_loader.dataset)
    accuracy = 100. * correct / len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        accuracy))
       
    ####################
    # visualize every epoch
    dataiter = iter(test_loader)
    images, labels = dataiter.next()
#    img_grid = tutils.make_grid(images)
#    plot_tensorboard(img_grid, one_channel=False)
    writer.add_figure('one batch of images', plot_tensorboard(model, vnet, images.cuda(), labels.cuda()), global_step=epoch+1)
    #writer.add_embedding(features,
    #                    metadata=class_labels,
    #                    label_img=images)

    return accuracy

# train model without LNL
def train_basic(train_loader,model, optimizer_model,epoch):
    print('\nEpoch: %d' % epoch)
    model.train()

    # remove meta_loss, train_meta_loader_iter
    train_loss = 0
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        
        inputs, targets = inputs.to(device), targets.to(device)
        
        outputs = model(inputs)
        # loss
        loss = criterion(outputs, targets)

        optimizer_model.zero_grad()
        loss.backward()
        optimizer_model.step()      ###

        train_loss += loss.item()
        prec_train = accuracy(outputs.data, targets.data, topk=(1,))[0]
        if (batch_idx + 1) % 50 == 0:
            print('Epoch: [%d/%d]\t'
                  'Iters: [%d/%d]\t'
                  'Loss: %.4f\t'
                  'Accuracy_TrainData@1 %.2f\t' % (
                      (epoch + 1), args.epochs, batch_idx + 1, len(train_loader.dataset)/args.batch_size,
                      (train_loss / (batch_idx + 1)), prec_train))

            writer.add_scalar('TrainLoss',
                            (train_loss / (batch_idx + 1)),
                            epoch * len(train_loader) + batch_idx)
            writer.add_scalar('Accuracy_TrainData',
                            prec_train,
                            epoch * len(train_loader) + batch_idx)


def train(train_loader,train_meta_loader,model, vnet,optimizer_model,optimizer_vnet,epoch):
    print('\nEpoch: %d' % epoch)

    train_loss = 0
    meta_loss = 0

    train_meta_loader_iter = iter(train_meta_loader)
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        model.train()
        inputs, targets = inputs.to(device), targets.to(device)
        meta_model = build_model().cuda()
        meta_model.load_state_dict(model.state_dict())
        outputs = meta_model(inputs)

        cost = F.cross_entropy(outputs, targets, reduce=False)
        cost_v = torch.reshape(cost, (len(cost), 1))
        v_lambda = vnet(cost_v.data)
        l_f_meta = torch.sum(cost_v * v_lambda)/len(cost_v)
        meta_model.zero_grad()
        grads = torch.autograd.grad(l_f_meta, (meta_model.params()), create_graph=True)
        meta_lr = args.lr * ((0.1 ** int(epoch >= 80)) * (0.1 ** int(epoch >= 100)))   # For ResNet32
        meta_model.update_params(lr_inner=meta_lr, source_params=grads)
        del grads

        try:
            inputs_val, targets_val = next(train_meta_loader_iter)
        except StopIteration:
            train_meta_loader_iter = iter(train_meta_loader)
            inputs_val, targets_val = next(train_meta_loader_iter)
        inputs_val, targets_val = inputs_val.to(device), targets_val.to(device)
        y_g_hat = meta_model(inputs_val)
        l_g_meta = F.cross_entropy(y_g_hat, targets_val)
        prec_meta = accuracy(y_g_hat.data, targets_val.data, topk=(1,))[0]


        optimizer_vnet.zero_grad()
        l_g_meta.backward()
        optimizer_vnet.step()         ###

        outputs = model(inputs)
        cost_w = F.cross_entropy(outputs, targets, reduce=False)
        cost_v = torch.reshape(cost_w, (len(cost_w), 1))
        prec_train = accuracy(outputs.data, targets.data, topk=(1,))[0]

        with torch.no_grad():
            w_new = vnet(cost_v)

        loss = torch.sum(cost_v * w_new)/len(cost_v)

        optimizer_model.zero_grad()
        loss.backward()
        optimizer_model.step()      ###


        train_loss += loss.item()
        meta_loss += l_g_meta.item()


        if (batch_idx + 1) % 50 == 0:
            print('Epoch: [%d/%d]\t'
                  'Iters: [%d/%d]\t'
                  'Loss: %.4f\t'
                  'MetaLoss:%.4f\t'
                  'Accuracy_TrainData@1 %.2f\t'
                  'Accuracy_MetaData@1 %.2f' % (
                      (epoch + 1), args.epochs, batch_idx + 1, len(train_loader.dataset)/args.batch_size,
                      (train_loss / (batch_idx + 1)),(meta_loss / (batch_idx + 1)), prec_train, prec_meta))

            writer.add_scalar('TrainLoss',
                            (train_loss / (batch_idx + 1)),
                            epoch * len(train_loader) + batch_idx)
            writer.add_scalar('MetaLoss',
                            (meta_loss / (batch_idx + 1)),
                            epoch * len(train_loader) + batch_idx)
            writer.add_scalar('Accuracy_MetaData',
                            prec_meta,
                            epoch * len(train_loader) + batch_idx)
            writer.add_scalar('Accuracy_TrainData',
                            prec_train,
                            epoch * len(train_loader) + batch_idx)


train_loader, train_meta_loader, test_loader = build_dataset()
# create model
model = build_model()
# for basic model (w/o LNL)
criterion = nn.CrossEntropyLoss().cuda()
vnet = None
if args.LNL == True:
    vnet = VNet(1, 100, 1).cuda()
    optimizer_vnet = torch.optim.Adam(vnet.params(), 1e-3,
                             weight_decay=1e-4)
    optimizer_model = torch.optim.SGD(model.params(), args.lr,
                                  momentum=args.momentum, weight_decay=args.weight_decay)
else:
    optimizer_model = torch.optim.SGD(model.parameters(), args.lr,
                                  momentum=args.momentum, weight_decay=args.weight_decay)

if args.dataset == 'cifar10':
    num_classes = 10
if args.dataset == 'cifar100':
    num_classes = 100

def matplotlib_imshow(img, one_channel=False):
    if one_channel:
        img = img.mean(dim=0)
    img = img /2 + 0.5

    npimg = img.numpy()
    if one_channel:
        plt.imshow(npimg, cmap="Greys")
    else:
        plt.imshow(np.transpose(npimg, (1,2,0)))

# to visualize
def select_n_random(data, labels, n=100):
    assert len(data) == len(labels)

    perm = torch.randperm(len(data))
    return data[perm][:n], labels[perm][:n]

def plot_tensorboard(model, vnet, images, labels):
    meta_model = build_model().cuda()
    meta_model.load_state_dict(model.state_dict())
    output = meta_model(images)
    _, preds_tensor = torch.max(output, 1)
    preds_tensor = preds_tensor.detach().cpu()
    preds = np.squeeze(preds_tensor.numpy())
    probs = [F.softmax(el, dim=0)[i].item() for i, el in zip(preds, output)]

    cost = F.cross_entropy(output, labels, reduce=False)
    CE_ = F.cross_entropy(labels-(10^-5), output, reduce=False)
    cost_v = torch.reshape(cost, (len(cost), 1))
    if vnet is None:
        weight = -100     # when LNL is not applied
    else:
        v_lambda = vnet(cost_v.data)
        v_lambda = v_lambda.cpu().detach().numpy()

    images = images.detach().cpu()
    plots = len(labels)
    fig = plt.figure(figsize=(20,35))
    plt.title("Predicted #0 with probs #1, GT #2, learned weight #3")
    for idx in np.arange(plots):
        ax = fig.add_subplot(plots//8,9, idx+1, xticks=[], yticks=[])
        matplotlib_imshow(images[idx], one_channel=False)
        # predicted class, loss, gt, weight(v_lambda)
        if vnet is not None:
            ax.set_title("{0} {1} {2} {3:.2f} {4}".format(
                preds[idx],
                round(probs[idx],2),
                labels[idx],
                v_lambda[idx][0],
                round(CE_[idx], 2)
            ))
        else:
            ax.set_title("{0} {1} {2} _ {4}".format(
                preds[idx],
                round(probs[idx],2),
                labels[idx],
                round(CE_[idx], 2)
            ))

    
    return fig

def main():
    global t_type, m_type, m_rate, t_rate, infoname
    best_acc = 0
    results = []
    for epoch in range(args.epochs):
        adjust_learning_rate(optimizer_model, epoch)
        test_acc = test(model=model, vnet=vnet, test_loader=test_loader, epoch=epoch)
        
        # select LNL or not
        print("flag", args.LNL)
        if args.LNL == True:
            train(train_loader,train_meta_loader,model, vnet,optimizer_model,optimizer_vnet,epoch)
        else:
            train_basic(train_loader,model,optimizer_model,epoch)
        
        test_acc = test(model=model, vnet=vnet, test_loader=test_loader, epoch=epoch)
        if test_acc >= best_acc:
            best_acc = test_acc

        results.append(test_acc)
        # write test acc
        writer.add_scalar('TestAccuracy',
                        test_acc,
                        epoch)
        print("EPOCH " + str(test_acc))

    print('best accuracy:', best_acc)

    #-------- write result file------
    # select LNL or not

    timestr = "./results/" + args.dataset + infoname
    with open(timestr+'.txt', 'w') as f:
        f.write("Dataset:" + args.dataset + '\n')
        if args.LNL == True:
            f.write("Meta Label Corruption" + m_type + m_rate + '\n')
        f.write("Train Label Corruption" + t_type + t_rate + '\n')
        for i in range(len(results)):
            f.write("%s " % round(results[i],5))

if __name__ == '__main__':
    main()
