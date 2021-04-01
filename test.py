import random

from googletrans import Translator
import wikipedia

def google_search(search_text):
    translator = Translator()
    result = ''
    search_data = search_text
    logger.info("google_search : "+search_data)
    if "who is" in search_data or "who are" in search_data:
        search_data = search_data.split(" ")[2:]
        search_data = " ".join(search_data)
        try:
            result = wikipedia.summary(search_data, sentences=2)
        except Exception as e:
            pass
    else:
        url = "https://www.google.co.in/search?q="+search_data
        logger.info("google_search : URL : "+url)
        try:
            search_result = requests.get(url).text
            soup = BeautifulSoup(search_result, 'html.parser')

            result_div = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')

            if "born" in search_data:
                for i in result_div:
                    s = translator.translate(dest='en', text = i.text)
                    a = str(s).split("=")[3].split(",")
                    b = a[:len(a)-1]
                    b = " ".join(b)

                    if "Born" in b:
                        result = b.split(":")[1:].__str__().replace("[' ","").replace("']","")
                        #print(result)
                        break

            else:
                for i in result_div:
                    s = translator.translate(dest='en', text=i.text)
                    a = str(s).split("=")[3].split(",")
                    b = a[:len(a) - 1]
                    result = " ".join(b)
                    #print(result)
                    break
        except Exception as e:
            pass 
    logger.info("google_search : Search Result ::"+result)
    return result

print(google_search("who is narendra modi"))