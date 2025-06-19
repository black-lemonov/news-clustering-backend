import asyncio

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

from src.config import SUMMARY_SIZE
from src.dependencies import get_parsers


def summarize(text: str) -> str:
    sentences_in_summary = SUMMARY_SIZE

    parser = PlaintextParser.from_string(text, Tokenizer("russian"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences_in_summary)

    return ' '.join([str(sent) for sent in summary])


async def parse_all():
    await asyncio.gather(*[p.parse() for p in get_parsers()])
