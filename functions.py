
def filter_keywords(text,keywords):
    #words to be removed
    question=['what','when','why','which','who','how','whose','whom']
    common_words=['the','a','an','am','is','may','can','will','do','say','go','get','make','know','think','take','come','want','look','use','find','give','tell']
    adverb=['now','also','not','as','up','here','there','so','very','immediately','initially','additionally','nearby','extremly','greatly','work','life','world','day','back']
    pronoun=['i','you','your','he','she','them','their','her','him','me','my','it','its','our','these','this','that','those','who','what','which']
    extra=['all','just','even','first','many','one','two','some','like','other','more','new','any','down','and','or','it','because','but','then','of','in','to','for','with','on','by','out','into','about','please']
    more=['done','free']
    not_values=question+common_words+adverb+pronoun+extra+more+keywords
    splited_text=text.split()
    result_text= [word for word in splited_text if word.lower() not in not_values]
    return ' '.join(result_text)
