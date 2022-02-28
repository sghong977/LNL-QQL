#TEST 5

logpath='logs/'
gpu_num=6
dataset=cifar100

seed=0

LNL_flag=True
LNL=" --LNL True"  

meta_rate=(0.1 0.3 0.6)
train_rate=(0.1 0.3 0.6)
meta_type=(unif unif unif)
train_type=(unif unif unif)

i=0
for i in "${!meta_rate[@]}"; do
    CUDA_VISIBLE_DEVICES=$gpu_num python MW-Net.py $LNL --dataset $dataset --corruption_type_meta ${meta_type[$i]} --corruption_type_train ${train_type[$i]} --corruption_prob_meta ${meta_rate[$i]} --corruption_prob_train ${train_rate[$i]} --seed $seed > logs/$dataset$LNL_flag${meta_type[$i]}${meta_rate[$i]}${train_type[$i]}${train_rate[$i]}$seed.txt
done