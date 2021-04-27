import pandas as pd
from tqdm.notebook import tqdm
import random
from sklearn.model_selection import train_test_split
from card_dataset import CardDataset
from tokenizers import Tokenizer, ByteLevelBPETokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.normalizers import Lowercase, NFD, StripAccents, Sequence
from transformers import CTRLLMHeadModel, CTRLConfig, CTRLTokenizer
from transformers import GPT2LMHeadModel, GPT2Config, GPT2Tokenizer
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling

def main(model_name):
    random.seed(0)

    cards_df = pd.read_csv('cards.csv')
    cards_df = cards_df.drop('name', axis=1)
    cards_df.head()

    cards_train, cards_val = train_test_split(cards_df, test_size=0.2)
    
    custom_tokens = ["\"<card>", "</card>\"", "<line>", "<precolon>", "</precolon>", "<color>", "</color>", "<bullet>"]

    bpe_tokenizer = ByteLevelBPETokenizer()

    bpe_tokenizer.pre_tokenizer = Whitespace()
    bpe_tokenizer.normalizer = Sequence([NFD(), Lowercase(), StripAccents()])
    bpe_tokenizer.add_tokens(custom_tokens)

    bpe_tokenizer.train(['training.txt', 'val.txt'], min_frequency=2)

    vocab_file, merges_file = tuple(bpe_tokenizer.save_model('.'))

    tokenizer = GPT2Tokenizer(vocab_file, merges_file)
    tokenizer.pre_tokenizer = Whitespace()
    tokenizer.normalizer = Sequence([NFD(), Lowercase(), StripAccents()])
    tokenizer.add_special_tokens({
        'pad_token': '<pad>',
        'unk_token': '<unk>'
    })
    tokenizer.add_tokens(custom_tokens)

    config = GPT2Config(
        vocab_size=len(tokenizer),
        n_positions=512,
        n_ctx=512,
        n_embd=768,
        n_layer=12,
        n_head=12
    )

    model = GPT2LMHeadModel(config)

    train_dataset = CardDataset(cards_train, tokenizer)
    validation_dataset = CardDataset(cards_val, tokenizer)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    args = TrainingArguments(
        output_dir='./results',          # output directory
        num_train_epochs=3,              # total number of training epochs
        per_device_train_batch_size=1,   # batch size per device during training
        per_device_eval_batch_size=1,    # batch size for evaluation
        warmup_steps=500,                # number of warmup steps for learning rate scheduler
        weight_decay=0.01,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=250,               # how frequently to log
        save_steps=500,                  # how frequently to save
        save_total_limit=2,              # total number of instances to save
        do_eval=True                     # compute evaluation
    )

    trainer = Trainer(
        model=model,                     # the instantiated 🤗 Transformers model to be trained
        args=args,                       # training arguments, defined above
        data_collator=data_collator,     # data collator
        train_dataset=train_dataset,     # training dataset
        eval_dataset=validation_dataset  # evaluation dataset
    )

    tokenizer.save_pretrained(f"{model_name}-tokenizer")
    trainer.train()
    trainer.save_model(model_name)
    trainer.evaluate()

if __name__ == "__main__":
    model_name = "gpt2-epochs3"
    main(model_name)