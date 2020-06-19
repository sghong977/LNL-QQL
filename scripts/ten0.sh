#TEST 0

logpath='logs/'
gpu_num=7
dataset=cifar10

seed=0

LNL_flag=False
LNL=""    #" --LNL "    

meta_rate=(0.0 0.0 0.0)   # X
train_rate=(0.1 0.3 0.6)
meta_type=(clean clean clean) # X
train_type=(flip flip flip)

i=0
for i in "${!meta_rate[@]}"; do
    CUDA_VISIBLE_DEVICES=$gpu_num python MW-Net.py $LNL --dataset $dataset --corruption_type_meta ${meta_type[$i]} --corruption_type_train ${train_type[$i]} --corruption_prob_meta ${meta_rate[$i]} --corruption_prob_train ${train_rate[$i]} --seed $seed > logs/$LNL_flag${meta_type[$i]}${meta_rate[$i]}${train_type[$i]}${train_rate[$i]}$seed.txt
done