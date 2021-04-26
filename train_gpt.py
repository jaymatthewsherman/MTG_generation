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
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling

def main():
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

    tokenizer = CTRLTokenizer(vocab_file, merges_file)

    encoding = tokenizer.encode("creature", return_tensors="pt")

if __name__ == "__main__":
    main()