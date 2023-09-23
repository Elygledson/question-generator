import random
import nltk
import spacy
from nltk import tokenize
from transformers import AutoModelForCausalLM, AutoTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import string


nlp = spacy.load("pt_core_news_lg")

tokenizer = AutoTokenizer.from_pretrained(
    "pierreguillou/gpt2-small-portuguese")
model = AutoModelForCausalLM.from_pretrained(
    "pierreguillou/gpt2-small-portuguese")
tokenizer.model_max_length = 1024
model.eval()


class BooleanQuestion:
    @staticmethod
    def get_verbs(sentence):
        doc = nlp(sentence)
        verbs = []
        for _, token in enumerate(doc):
            if token.pos_ == "VERB" and len(list(token.children)) > 1:
                verbs.append(token.text)
        return verbs

    @staticmethod
    def get_noun(doc):
        noun_phrases = []
        for chunk in doc.noun_chunks:
            noun_phrases.append(chunk.text)
        return noun_phrases

    def get_best_sentence(self, verbs, current_sentence):
        if len(verbs) >= 2:
            indice = current_sentence.find(verbs[-2])
        else:
            indice = current_sentence.find(verbs[-1])
        phrase_cut = current_sentence[:indice].strip()
        return phrase_cut

    def get_sentences(self, text):
        sentence_starts = [
            token.i for token in text if token.is_sent_start]
        sentences = []
        for idx in range(0, len(sentence_starts)):
            if idx < len(sentence_starts) - 1:
                sentences.append(
                    str(text[sentence_starts[idx]:sentence_starts[idx + 1]]))
            else:
                sentences.append(
                    str(text[sentence_starts[idx]:len(text)]))
        return sorted(sentences, key=lambda frase: len(frase))

    def get_ids_and_max_length(self, current_sentence):
        verbs = self.get_verbs(current_sentence)
        best_sentence = self.get_best_sentence(verbs, current_sentence)
        input_ids = tokenizer.encode(best_sentence, return_tensors='pt')
        maximum_length = len(best_sentence.split()) + 40
        return input_ids, maximum_length, current_sentence

    def outputs(self, input_ids, maximum_length, sentences_num):
        sample_outputs = model.generate(
            input_ids,
            do_sample=True,
            max_length=maximum_length,
            top_p=0.80,
            top_k=30,
            repetition_penalty=10.0,
            num_return_sequences=sentences_num
        )
        return sample_outputs

    def get_question_sentence(self, sentences):
        idx = random.randint(0, len(sentences) - 1)
        return sentences.pop(idx)

    def count_key_words(self, sequence):

        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')

        tokens = word_tokenize(sequence)

        # Lista de palavras-chave irrelevantes (stop words)
        stop_words = set(stopwords.words('portuguese'))
        stop_words.update(string.punctuation)

        keys = []
        # Análise morfológica e filtragem
        for token, tag in pos_tag(tokens):
            if token.lower() not in stop_words and tag.startswith('N'):
                keys.append(token)

        return len(keys)

    def generate(self, text, sentences_num=3):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        text = nlp(text)

        sentences = self.get_sentences(text)
        sentences_by_keyswords = {}
        for idx, sentence_temp in enumerate(sentences):
            keys_count = self.count_key_words(sentence_temp)
            sentences_by_keyswords[idx] = keys_count

        sentences_by_keyswords = dict(
            sorted(sentences_by_keyswords.items(), key=lambda item: item[1], reverse=True))

        keys = list(sentences_by_keyswords.keys())
        final, generated_sentences = [], []

        count = 0
        while count < sentences_num and len(keys) > 0:
            current_sentence = sentences[keys.pop(0)]
            input_ids, maximum_length, current_sentence = self.get_ids_and_max_length(
                current_sentence)
            sample_outputs = self.outputs(
                input_ids, maximum_length, sentences_num)
            for _, sample_output in enumerate(sample_outputs):
                decoded_sentence = tokenizer.decode(
                    sample_output, skip_special_tokens=True)
                final_sentence = tokenize.sent_tokenize(decoded_sentence)[0]
                generated_sentences.append(final_sentence)

            generated_sentences.append(current_sentence)
            count += 1

        for idx in range(sentences_num):
            question = self.get_question_sentence(generated_sentences)
            boolean_answer = question == current_sentence
            final.append({'question': question, 'answer': boolean_answer})
        return final
