from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import pipeline

class GPTGenerator:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = GPT2LMHeadModel.from_pretrained(f"./models/{self.model_name}")
        self.tokenizer = GPT2Tokenizer.from_pretrained(f"./models/{self.model_name}-tokenizer")

        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        self.end_token = "</card>\""

    def generate_until_eoc(self, prompt, max_length=512):
        while len(prompt) < max_length:
            prompt = self.generator(prompt, do_sample=True, max_length=max_length)[0]['generated_text']
        if self.end_token in prompt:
            return prompt[:prompt.index(self.end_token) + len(self.end_token)]
        return prompt

    def generate(self, rarity, colors, card_type, cost, power=None, toughness=None, loyalty=None):
        inputs = [rarity, colors, card_type, cost]
        if card_type.lower() == "creature":
            inputs.extend([power, toughness])
        elif card_type.lower() == "planeswalker":
            inputs.append(loyalty)
        inputs.append("\"<card>")
        prompt = " ".join(inputs)

        return self.generate_until_eoc(prompt)
    
if __name__ == "__main__":
    model_name = "gpt2-epochs3"
    card_generator = GPTGenerator(model_name)
    print(card_generator.generate("rare", "G", "Sorcery", "MG"))