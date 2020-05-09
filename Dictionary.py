"""
author:sqa
time:2020/5/7 10:48
function:用于定义单词类以及设计各种函数
"""
import pymongo

# 数据库初始化操作
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
# database
dictionary_database = my_client["dictionary"]
# collection
dictionary_content = dictionary_database["content"]


# word class
class Word(object):

    def __init__(self, word, part_of_speech, meaning, example=None, **kwargs):
        """

        :param word: spelling
        :param part_of_speech:n,v,adj...
        :param meaning: the meaning of the word
        :param example:example sentences
        """
        self.word = word
        self.part_speech = part_of_speech
        self.meaning = meaning
        self.example = example
        self.others = kwargs

    def to_dict(self):
        return self.__dict__


def delete_words(word_name):
    """

    :param word_name: 删除的单词
    用于删除数据库中的单词
    """
    try:
        if list(dictionary_content.find({'word': word_name})):
            dictionary_content.delete_one({'word': word_name})
            print('删除成功')
        else:
            raise ValueError
    except ValueError:
        raise ValueError("无该单词")


def add_words(word: Word):
    """

    :param word: 插入的单词
    用于单词插入
    """
    try:
        if not list(dictionary_content.find({'word': word.word})):
            dictionary_content.insert_one(word.to_dict())
            print('插入成功')
        else:
            raise ValueError
    except ValueError:
        raise ValueError("重复插入相同单词")


def refresh_words(old_word_name, refresh_content):
    """

    :param old_word_name: 要更改的单词
    :param refresh_content: 更新内容
    """
    word_content = dictionary_content.find_one({'word': old_word_name})
    print(word_content)
    try:
        if word_content:
            dictionary_content.update_one(word_content, {'$set': refresh_content})
            print('更新成功')
        else:
            raise ValueError
    except ValueError:
        raise ValueError('未找到相关单词')


def inquire_words(word_name):
    """

    :param word_name: 查询的单词内容
    :return:返回一个单词的基本信息
    """
    word_content = dictionary_content.find_one({'word': word_name})
    # print(word_content)
    return word_content


def scan_words():
    """
    :return:返回所有信息基本信息
    """
    # print(list(dictionary_content.find()))
    return list(dictionary_content.find())


# def main():
    # word = Word('hello', 'v', '你好那', 'hello,nice to meet you', yongfa='beijing')
    # add_words(word)
    # delete_words(word_name='hello')
    # refresh_words('hello', word)
    # inquire_words('hello')
    # scan_words()

#
# if __name__ == '__main__':
    # main()
