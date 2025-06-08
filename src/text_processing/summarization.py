from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from razdel import sentenize

from src.config import SUMMARY_SHRINK


def summarize(text: str) -> str:
    sentences_in_source = len([sent for sent in sentenize(text)])
    sentences_in_summary = sentences_in_source // SUMMARY_SHRINK

    parser = PlaintextParser.from_string(text, Tokenizer("russian"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences_in_summary)

    return ' '.join([str(sent) for sent in summary])


if __name__ == "__main__":
    text = "Сообщалось, что большинство пассажиров маршрута «улица Московская — улица Петра Кононыхина» — школьники, пассажиропоток летом становится меньше, поэтому необходимости в 10 автобусах нет.  Однако местные жители высказались против таких изменений — по их словам, этот маршрут служит в качестве пересадочного на автобусы по Российской и Петра Метальникова, а также на трамваи на Московской. В связи с этим в департаменте транспорта и дорожного хозяйства Краснодара сообщили, что с 1 июля по маршруту № 66 продолжат курсировать автобусы.  В будние дни будут ходить 10 автобусов с 6:15 до 22:15, интервал — 5-10 минут. По субботам на линию выйдут 8 водителей с 6:30 до 22:05, интервал — 5-10 минут. По воскресеньям и в праздники ходить по маршруту будут 4 автобуса с 6:30 до22:10, интервал — 20-30 минут, сообщает пресс-служба дептранса Краснодара. Читайте также: в Краснодаре открыли по вопросам работы кондиционеров в транспорте."
    print(summarize(text))
