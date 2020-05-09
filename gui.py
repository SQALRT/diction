"""
author:sqa
time:2020/5/7 17:20
用于主界面设计
"""
from Dictionary import *
import easygui as g
choices = ['添加单词',
           '删除单词',
           '更新单词信息(自动保存)',
           '查询单词信息',
           '浏览所有单词',
           '导入导出词库',
           '我的查词记录',
           '复习']
add_fields = ['单词',
              '词性',
              '中文释义',
              '典型例句']
history_content = dictionary_database["history"]
while 1:
    g.msgbox('嗨，欢迎进入我的字典')
    choice = g.choicebox(msg='您希望进行哪些操作呢？',
                         choices=choices)
    # print(choice)
    if choice == '添加单词':
        word_info = g.multenterbox(msg='单词信息', fields=add_fields)
        # print(word_info)
        word = Word(word_info[0], word_info[1], word_info[2], word_info[3])
        add_words(word)
        g.msgbox('添加成功')
    elif choice == '删除单词':
        word = g.enterbox(msg='删除的单词')
        # print()
        g.msgbox('确定要删除吗？')
        delete_words(word)
        g.msgbox('删除成功')
    elif choice == '更新单词信息(自动保存)':
        word = g.enterbox(msg='要更新的单词')
        word_info = g.multenterbox(msg='单词信息', fields=add_fields)
        # print(word_info)
        word_content = Word(word_info[0], word_info[1], word_info[2], word_info[3])
        refresh_words(word, word_content.to_dict())
    elif choice == '查询单词信息':
        try:
            word = g.enterbox(msg='要查询的单词信息')
            word_info = inquire_words(word)
            g.msgbox('单词:{} 词性:{} 中文释义:{}'.format(
                word_info['word'], word_info['part_speech'], word_info['meaning']
            ))
            if not list(history_content.find({'word': word_info['word']})):
                word_info['time'] = 1
                history_content.insert_one(word_info)
            else:
                word_content = history_content.find_one({'word': word})
                history_content.update_one(word_content, {'$set': {'time': word_content['time']+1}})

        except TypeError:
            g.msgbox('没有该单词')
    elif choice == '浏览所有单词':
        words = scan_words()
        words_list = []
        for word_info in words:
            words_list.append('单词:{} 词性:{} 中文释义:{}\n'.format(
                word_info['word'], word_info['part_speech'], word_info['meaning']))
        g.textbox(text=words_list)
    elif choice == '导入导出词库':
        words = scan_words()
        choice = g.buttonbox(msg='选择你想要进行的操作', choices=['导入词库', '导出词库'])
        if choice == '导出词库':
            path = g.diropenbox()
            # print(path)
            try:
                f = open(path+'/dictionary.txt', 'w')
                try:
                    for word in words:
                        f.write(str(word)+'\n')
                except IOError as e:
                    g.msgbox('文件导入异常')
                finally:
                    f.close()
            except IOError:
                g.msgbox('打开文件异常')

        else:
            import_list = []
            path = g.fileopenbox()
            try:
                f = open(path, 'r')
                try:
                    for line in f:
                        import_list.append((eval(line)))
                except IOError as e:
                    g.msgbox('文件读取异常')
                finally:
                    f.close()
            except IOError:
                g.msgbox('文件打开异常')
            for word in import_list:
                try:
                    if not list(dictionary_content.find({'word': word['word']})):
                        dictionary_content.insert_one(word)
                        print('插入成功')
                    else:
                        continue
                except KeyError:
                    print('没有按照规范建立欲导入的词库')
            g.msgbox('导入成功')
    elif choice == '我的查词记录':
        words = list(history_content.find())
        words_list = []
        for word_info in words:
            words_list.append('单词:{} 词性:{} 中文释义:{} 查询次数:{}\n'.format(
                word_info['word'], word_info['part_speech'], word_info['meaning'],word_info['time']))
        g.textbox(text=words_list)
    elif choice == '复习':
        while 1:
            words = list(history_content.find())
            word = g.choicebox(msg='单词列表', choices=[word_info['word'] for word_info in words])
            word_info = inquire_words(word)
            try:
                g.msgbox('单词:{} 词性:{} 中文释义:{}'.format(
                    word_info['word'], word_info['part_speech'], word_info['meaning']
                ))
            except TypeError:
                break
    # a = g.ccbox('还要继续吗？', choices=['继续', '退出'])
    # print(a)
    if not g.ccbox('还要继续吗？', choices=['继续', '退出']):
        # print(1)
        break
    else:
        continue
