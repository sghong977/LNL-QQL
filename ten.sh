#CUDA_VISIBLE_DEVICES=4 python MW-Net.py --corruption_type flip --dataset cifar10 --corruption_prob 0.6

logpath='logs/'
gpu_num=4
dataset=CIFAR10

seed=(0 0 0 0)
rate=(0.6 0.6 0.6 0.6)
type=(unif flip flip2 hierarchical)
i=0

for i in "${!seed[@]}"; do
    CUDA_VISIBLE_DEVICES=$gpu_num python MW-Net.py --dataset $dataset --corruption_type $type --corruption_prob $rate --seed $seed >> $type$rate$seed.txt
done