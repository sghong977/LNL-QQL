#TEST 2

logpath='logs/'
gpu_num=5
dataset=cifar100

seed=0

LNL_flag=True
LNL=" --LNL True"  

meta_rate=(0.0 0.0 0.0)
train_rate=(0.1 0.3 0.6)
meta_type=(clean clean clean)
train_type=(flip flip flip)

i=0
for i in "${!meta_rate[@]}"; do
    CUDA_VISIBLE_DEVICES=$gpu_num python MW-Net.py --dataset $dataset $LNL --corruption_type_meta ${meta_type[$i]} --corruption_type_train ${train_type[$i]} --corruption_prob_meta ${meta_rate[$i]} --corruption_prob_train ${train_rate[$i]} --seed $seed > logs/$dataset$LNL_flag${meta_type[$i]}${meta_rate[$i]}${train_type[$i]}${train_rate[$i]}$seed.txt
done