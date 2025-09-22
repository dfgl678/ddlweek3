Training GPT2 Chinese from zero to hero
==

1.Description:
---
从头训练一个82M的中文GPT2模型，使用BERT的Tokenizer.中文语料采用龙族小说的部分章节，大小约6M。训练21个周期，batchsize=4。最终可以续写10句以上的龙族小说。此处仅上传部分改动/重要文件。其他文件参考https://github.com/lvfinn/chinese-GPT2-start-from-zero。

2.Start:
----
(1)***environment***

首先，我们下载依赖。
```bash
pip install -r requirements.txt
```

(2)***dataset***

准备中文语料（以txt.形式），放置在./data/文件夹下，在clr_ctrl.py中添加代码将.txt文件更改为input.json文件

按照参考样例./train.json更改input.json文件格式,由于数据集内容为原始的小说内容，包含着大量的非法字符和json读取不支持的控制字符，因此我们对原始数据集文件进行处理，去除其中非法字符，生成预处理好的数据集文件train.json。
```bash
python clr_ctrl.py
```

(3)***Model***

在model_config 定义初始GPT-2模型的超参数配置，
- "initializer_range": 0.02 ： 定义了模型参数（如权重矩阵）在初始化时的标准差，权重会在均值为0，标准差为0.02的正态分布中进行随机初始化。
- "layer_norm_epsilon": 1e-05 ： 用于层归一化的常数，用于避免在归一化过程中出现除以零的情况。设置值为1e-05，用于稳定训练。
- "n_ctx": 1024 ： 表示模型上下文窗口的大小，GPT-2 在生成文本时会考虑的最大序列长度。最大长度设为1024，即模型一次最多能处理1024个 token。
- "n_embd": 768 ： 表示每个token的嵌入维度大小，即模型中词向量的维度。设置为768，即每个词汇的表示向量是768维的。
- "n_head": 12 ： 表示自注意力机制中的注意力头的数量。设置为12，即模型的多头注意力机制中有12个独立的头。
- "n_layer": 10 ： 表示 Transformer 编码器中的层数。在这里，设置为 12，即模型有 12 层堆叠的 Transformer 块。
- "n_positions": 1024 ： 表示模型可以处理的最大位置索引，即序列中的最大位置数。最大位置数为 1024，和 n_ctx一致，表示模型最多能处理1024个位置的token。
- "vocab_size": 13317 ： 表示词汇表的大小，即模型可以识别和生成的词汇数量。在这里，词汇表大小为 21128，表示该模型可以处理的词汇量为21128个不同的 token。


(4)***Training***

现在，我们可以使用我们处理好的数据集来训练我们的初始gpt2模型，使用如下命令：
```bash
python train.py   --model_config config/model_config_small.json   --tokenized_data_path data/tokenized/   --tokenizer_path cache/vocab_small.txt   --raw_data_path data/train.json   --epochs 15   --log_step 200   --stride 512   --output_dir model/   --device 0,1   --num_pieces 100   --raw
```

在这个过程中，我们可以看到命令窗口打印出模型的config文件，定义了模型的结构；同时也打印出了模型的参数量，为81894144，约82M

Print Model config
config:
{
  "attn_pdrop": 0.1,
  "embd_pdrop": 0.1,
  "finetuning_task": null,
  "initializer_range": 0.02,
  "layer_norm_epsilon": 1e-05,
  "n_ctx": 1024,
  "n_embd": 768,
  "n_head": 12,
  "n_layer": 10,
  "n_positions": 1024,
  "num_labels": 1,
  "output_attentions": false,
  "output_hidden_states": false,
  "output_past": true,
  "pruned_heads": {},
  "resid_pdrop": 0.1,
  "summary_activation": null,
  "summary_first_dropout": 0.1,
  "summary_proj_to_labels": true,
  "summary_type": "cls_index",
  "summary_use_proj": true,
  "torchscript": false,
  "use_bfloat16": false,
  "vocab_size": 13317
}
number of parameters: 81894144

训练过程中，每个epoch对应的模型都将存储在./model/目录下，最终训练好的模型将存储在./model/final_model/路径中。

(5)***Generate***

现在，我们可以使用我们用目标语料训练生成的模型来进行文字生成，使用如下命令：
```bash
python generate.py   --device 1   --length 1000   --tokenizer_path cache/vocab_small.txt   --model_path model/final_model   --prefix "[CLS]萧炎大喝一声"   --topp 1   --temperature 1.0 --save_samples --save_samples_path ./mnt/
```

3.Result
--
最终会生成10个文字样本，存储在samples中，其中之一如下：

======================================== SAMPLE 1 ========================================

路明非望着她的眼睛，他的眼睛里有着一丝哀伤。“你怎么知道的？”源稚女抬头看着恺撒，目光迷离地点头。“我们的意思是电梯门打开了，那是电梯门打开这个大楼层楼，我们在高天原的方不方移动，电梯也可以直接上方的建筑
”恺撒说，“我刚从下一层开始到达了高层去。”楚子航说。“电梯门打开的那一层大约是24层，就是三层楼，高层楼的保险设计标准，二十层。所有4层以二层。”楚子航说。“这一层建造所的建造所，还有4层建造所的建筑物是三   
层，从电梯开那座建造所有。”“我用的高层建造所建造所的进口也就是当贵宾电梯井的货运级数字塔，还是4层是第一个走域，路如果是源氏重工那座大约441层中的货运电梯。”源稚生看了一眼行电梯。“如果这一层建筑实是橘政 
宗，这一层建造所的货运电梯也经就是二层。”楚子航摇了摇头，“如果是他们也没有人也没有通往这一层，如果源氏重工里区建造所承载塔的楼层。这座老式建造所的货运电梯也就是五十级来源氏重工。”“你建造所谓的这座地震 
，要从电梯也没有这座楼层去看电梯井，要命也没有可能到达三层，所以每层还有五十二十二根。”橘政宗点了足点遗嘱跟这座电梯的这座房价，也没有五十层建筑建筑的建筑结构，还有这座大约能到好像恺撒那座二点。橘政宗也
什么问题，楼层建造那么花岗岩流研究所的建筑结构图，也就是第一的文字是第一层建筑，可以下这座老字是第一个“挖泉之哀悼”，“也就是第六个。”源稚生说。“是，橘政宗先生你们这一直在日本。”橘政宗笑，“是第一个中文文
？”“看书。”“是，所就是那个中文明一个。”橘政宗缓缓地说，“这说老人为什么都没有说。”橘政宗微微点头，“这是一个人选择了吧，说老爹，不过我们也没跟你们联系，不过我们怎么把这些细节拍下来，要是供帮你们搞得住   
，也没指面包括这笔也没有任何一点。”“确实说橘政宗也许大别添碗，不过要把这块土地址也扔进来么？”路明非说，“其中那是全世界上最有古代文明的东西，天假还有从古代，神社中把神代讲各种的故事件看作一些秘的。”橘政
把一张黑白布扔在桌上，“看这个俄国人里两千年代历史以神秘的名字，在俄语中，名叫‘中与历史’，一种颜色、中国人，一个称作者‘天赐，都被中带着惊世’。’源自己的真正的‘完美藏。”“那不是人用来画面？”楚子航问。“太太就是说，也许神话，它里面积累了。”恺撒说，“也许是。”路明非挠挠头，“我们从来没有过，一路明非，也许就是故意外人从神官员名单上退休的。”楚子航打开


==========================================================================================
