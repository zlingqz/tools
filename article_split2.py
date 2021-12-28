import copy
def ner_split(text: str, lenth):
    words = []
    symbol1 = ['\n','。','？','！','?','!']
    symbol2 = [';','；',',','，','、']
    if len(text) <= lenth:
        return [text]
    #elif len(text) < lenth:
    #    words.append(text)
    else:
        split_word = ''
        len_text = len(text)
        tag1 = -1
        tag2 = -1
        last_tag1_index = -1
        last_tag2_index = -1
        index = 0
        index0 = 0
        i = 1 
        while True:
            cur_word = text[index]
            if cur_word in symbol1:
                tag1 += 1
                last_tag1_index = index
            elif cur_word in symbol2:
                tag2 += 1
                last_tag2_index = index
            if index == len_text - 1 :
                split_word = text[index0: index + 1]
                words.append(split_word)
                break
            else:
                if i == lenth and tag1 >= 0:
                    split_word =text[index0: last_tag1_index + 1]
                    words.append(split_word)

                    index0 = last_tag1_index + 1
                    tag1 = -1
                    tag2 = -1
                    last_tag1_index = -1
                    i = 1

                elif i == lenth  and tag2 >= 0:
                    split_word = text[index0: last_tag2_index + 1]
                    words.append(split_word)
                    index0 = last_tag2_index + 1
                    index = last_tag2_index
                    tag2 = -1
                    i = 1

                elif i == lenth:
                    split_word =text[index0: index + 1]
                    words.append(split_word)
                    index0 = index + 1
                    tag1 = -1
                    tag2 = -1
                    i = 1

                else:
                    i += 1
                index += 1
    return words


if __name__ == '__main__':
    input_path = 'data/news_all_post.csv'
    output_path = 'data/news_all_split.csv'
    with open(input_path,'r',encoding='utf-8') as f, open(output_path,'w',encoding='utf-8') as f2:
        result_dict = {}
        for line in f:
            line_split = line.strip().split(',')
            if len(line_split) == 3:
                category, title, content = line_split
                sent_list = ner_split(content,256)
                for i in sent_list:
                    key = ','.join([category, title, i])
                    if key not in result_dict:
                        result_dict[key] = 1
                    #else:
                    #    result_dict[key] += 1
            else:
                print('error', line_split)

        for j in result_dict:
            f2.write(j + '\n')

