from flashtext import KeywordProcessor
from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline
import nltk.data
import pytextrank
import joblib
import string
import spacy
import pke


class FillBlankQuestion:
    def __init__(self) -> None:
        self.fill_mask = self.load_or_create_fill_mask_pipeline()

    def load_or_create_fill_mask_pipeline(self):
        try:
            return joblib.load("fill_mask_pipeline.joblib")
        except FileNotFoundError:
            model = AutoModelForMaskedLM.from_pretrained(
                'neuralmind/bert-large-portuguese-cased')
            tokenizer = AutoTokenizer.from_pretrained(
                'neuralmind/bert-large-portuguese-cased', do_lower_case=False)
            pipeline_instance = pipeline(
                'fill-mask', model=model, tokenizer=tokenizer)
            joblib.dump(pipeline_instance, "fill_mask_pipeline.joblib")
            return pipeline_instance

    def generate(self, text):
        keyword_processor = self.get_keyword_using_text_rank(text)
        sentences = self.tokenize_sentence(text)
        questions = self.get_questions(sentences, keyword_processor)
        return questions

    def tokenize_sentence(self, text):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        sentences = nltk.sent_tokenize(text)
        sentences = [sentence.strip()
                     for sentence in sentences if len(sentence) >= 20]
        return sentences

    def get_questions(self, sentences, keyword_processor):
        questions = []
        for _, sentence in enumerate(sentences):
            if '?' not in sentence:
                keywords_found = keyword_processor.extract_keywords(sentence)
                if keywords_found:
                    question = self.get_distractors_using_bert(
                        sentence, keywords_found)
                    questions.append(question)
        return questions

    def get_keyword_using_multi_partite_rank(self, text):
        extractor = pke.unsupervised.MultipartiteRank()
        stoplist = list(string.punctuation)
        stoplist += pke.lang.stopwords.get('pt')
        extractor.load_document(input=text,
                                stoplist=stoplist)
        pos = {'VERB', 'ADJ', 'NOUN'}
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
        keyphrases = extractor.get_n_best(n=10)
        keyword_processor = KeywordProcessor()
        for key, _ in keyphrases:
            keyword_processor.add_keyword(key)
        return keyword_processor

    def get_keyword_using_text_rank(self, text):
        keyword_processor = KeywordProcessor()
        nlp = spacy.load("pt_core_news_lg")
        nlp.add_pipe("textrank")
        doc = nlp(text)
        for phrase in doc._.phrases[:20]:
            keyword_processor.add_keyword(phrase.text)
        return keyword_processor

    def get_distractors_using_bert(self, sentence, keywords, options_num=10):
        mask_keyword = keywords[0].split()[-1]
        sentence = sentence.replace(mask_keyword, '[MASK]', 1)
        options = self.fill_mask(sentence, top_k=options_num)
        alternatives = set([mask_keyword])
        for option in options:
            option = option['token_str'].lower()
            if option not in list(string.punctuation):
                alternatives.add(option)

        return {'question': sentence.replace('[MASK]', '_____________'), 'options': list(alternatives), 'answer': mask_keyword}
