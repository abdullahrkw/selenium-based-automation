from __future__ import print_function
import os
import sys
import time
import threading

from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def post2convo(email="", pwd="", title="", text=""):
    """post message to convo by opening firefox in 
    headless mode. Also, note we are specifying JS 
    here to be run in broswer.
    """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://app.convo.com/")
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id ("password").send_keys(pwd)
    driver.find_element_by_id("btnSignIn").click()
    time.sleep(5)
    driver.find_element_by_id("inlineInsertPlaceholderText").click()
    driver.find_element_by_id("noteTitleField").send_keys(title)
    driver.find_element_by_id("ql-editor-1").send_keys(text)
    # Python raw string is created by prefixing a string literal with 'r' or 'R'. 
    # Python raw string treats backslash (\) as a literal character. 
    # This is useful when we want to have a string that contains backslash 
    # and don't want it to be treated as an escape character.
    browser_js = r'''
    function linkify(text) {
    let urlRegex =/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    return text.replace(urlRegex, function(url) {
        return '<a href=' + url + '>' + url + '</a>';
        });
    };
    let text = document.getElementById('ql-editor-1').innerHTML;
    document.getElementById('ql-editor-1').innerHTML = linkify(text);
    '''
    driver.execute_script(browser_js)
    driver.find_element_by_css_selector("button.btn-primary").click()
    driver.close()

app = Flask(__name__)
@app.route('/post2convo', methods=['POST'])
def request2post():
    """server generic post2convo POST request. Runs post2convo() 
    in separate thread.
    """
    json_request = request.get_json (force=True, silent=False, cache=True)
    threading.Thread(target=post2convo, args=(
     json_request["convo_email"],
     json_request["convo_pwd"],
     json_request["message_title"],
     json_request["message_text"])).start()
    return jsonify({"status": "OK"})

@app.route('/slack/post2convo', methods=['POST'])
def slack2convo():
    """server slack based post2convo POST request. Runs post2convo() 
    in separate thread. slack sends POST data in www-data-urlencoded 
    and not in json
    """
    slack_message = request.form["text"]
    slack_user_name = request.form["user_name"]
    convo_title = ""
    convo_message = slack_message
    if(slack_message.find("]") > slack_message.find("[")):
        convo_title = slack_message[slack_message.find("[") + 1 : slack_message.find("]")]
        m_index = slack_message.find("] ")
        if m_index != -1:
            convo_message = slack_message[m_index+1:]
    threading.Thread(target=post2convo, args=(
     os.environ["CONVO_EMAIL"],
     os.environ["CONVO_PWD"],
     convo_title,
     convo_message)).start()
    return jsonify({
        "Title": convo_title,
        "Message": convo_message,
        "response_type": "in_channel",
        "text":f"The following message posted by {slack_user_name} will be shared on convo by abdullah"})

if __name__ == '__main__':
   app.run(host=os.environ["HOST"], port=os.environ["PORT"], debug=False)
    