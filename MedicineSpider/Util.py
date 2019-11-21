
def remove_punc(text):
    return text.replace('\r' ,'').replace('\n' ,'').replace('\xa0', '').replace('   ', '').replace('\t' ,'')

def remove_punc_without_blank(text):
    return text.replace('\r' ,'').replace('\n' ,'').replace('\xa0', '').replace('\t' ,'')