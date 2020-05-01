#wml_python_function
def py_funct(params={}):
    try:
        # Import the subprocess module.
        import subprocess
        
        # Install required packages.
        subprocess.check_output('pip install --user lxml', stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output('pip install --user bs4', stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output('pip install --user sklearn', stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:        
        install_err = 'subprocess.CalledProcessError:\n\n' + 'cmd:\n' + e.cmd + '\n\noutput:\n' + e.output.decode()
        raise Exception( 'Installation failed:\n' + install_err )
    
    def score(payload):
        try:
            # Import required modules.
            from bs4 import BeautifulSoup
            from urllib.request import urlopen
            from sklearn.feature_extraction.text import CountVectorizer

            urls = payload['input_data'][0]['values']
            final_texts = []   # An array that will have stripped clean text from html tag enclosed text.

            for url in urls:            
                html = urlopen(url)
                soup = BeautifulSoup(html, 'lxml')

                p_tags = soup.find_all('p')    # Text is enclosed in <p> tag.

                for p in p_tags:
                    str_p = str(p)
                    text = BeautifulSoup(str_p, 'lxml').get_text()
                    final_texts.append(text)

            vectorizer = CountVectorizer()
            vectorizer.fit_transform(final_texts)

            return {"predictions": [{"fields": ["tokens"], "values": [vectorizer.get_feature_names()]}]}
        except Exception as e:
            return {"predictions": [{"error" : repr(e)}]}
        
    return score


score = py_funct()