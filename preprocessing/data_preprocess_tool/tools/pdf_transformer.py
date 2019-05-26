### Writen by Zengwei Wang
### date: Apr 10, 2019
### WARNING: default .pdf data resources should be under 'data' directory

from tika import parser
import os
import re
import json


data_path = './data/'

#reading .txt file by lines
def preprocess(content):
    #Page 1 of 15file:///Users/jas/srvr/apps/cs9315/18s2/lectures/week10/notes.html\n
    content = [ele for ele in content if not bool(re.match(r"Page.*file://.*notes.html\n",ele))]
    #4/10/18, 3)16 pmWeek 10 Lectures\n
    content = [ele for ele in content if not bool(re.match(r".*[a-z]mWeek.*",ele))]
    
    for i in range(len(content)):
        if bool(re.match(r".*[0-9]*/[0-9]*\n.*",content[i])):
            head_page = content[:i]
            header_stop = i
            break
    
    #get the content of first page
    header = [ele for ele in head_page if ele != '\n']
    header = {'topic':'header\n','content':' '.join(head_page).strip('\n ')+'\n'}
    print('header was finished.')
    #print(header['content'])
    dataset = [header]
    
    
    #get the rest content of lecture note
    spiliter = []
    for i in range(len(content)):
        if bool(re.match(r".*[0-9]*/[0-9]*\n.*",content[i])):
            spiliter.append(i)
    print('spiliter was finished.')
    for i in range(len(spiliter)):
        try:
            topic = content[spiliter[i]]
            comment = ' '.join(content[spiliter[i]+1:spiliter[i+1]])
            dataset.append({'topic': topic, 'content': comment})
        except:
            dataset.append({'topic': content[spiliter[i]], \
                            'content': ' '.join(content[spiliter[i]+1:])})
    print('dataset was finished.')
    return dataset

def get_text_files():
    #convert .pdf files to .txt files
    for i in range(1,11):
        try:
            if i < 10:
                week = 'week0'
            else:
                week = 'week'
            if not os.path.exists('./data_text/'):
                os.makedirs('./data_text/')
            files_adr =  data_path + week + str(i)+'.pdf'
            output_adr = './data_text/'+ week + str(i)+'.txt'

            raw = parser.from_file(files_adr)
            #print(raw['content'])
            with open(output_adr,'w') as f:
                f.write(raw['content'])
            print('week'+ str(i)+'completed')
        except:
            pass

def get_json_files():
    for i in range(1,11):
        try:
            if i < 10:
                week = 'week0'
            else:
                week = 'week'
            file_adr = './data_text/'+ week + str(i)+'.txt'

            with open(file_adr,'r') as f:
                content = f.readlines()
            # preprocessing funtion
            content = preprocess(content)
            if not os.path.exists('./data_preprocessed/'):
                os.makedirs('./data_preprocessed/')
            file_adr = './data_preprocessed/'+ week + str(i)+'.json' 

            with open(file_adr, 'w') as f:
                f.write('[\n')
                for tp in content:
                    f.write(json.dumps(tp, indent=1))
                    if tp is not content[-1]:
                        f.write(',\n')
                    else:
                        f.write('\n')
    #                 f.write(tp['topic'])
    #                 f.write('='*30 + '\n')
    #                 f.write(tp['content'])
    #                 f.write('='*31 + '\n')
                f.write(']\n')

        except:
            print('data ', i ,' was not finished.')

if __name__ == '__main__':
    #generate .txt files
    get_text_files()
    get_json_files()
        


