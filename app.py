import string
from urllib import response
from flask import Flask, jsonify, request
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import json
from urlextract import URLExtract


app = Flask(__name__)

with open("profanity.txt") as f:
    profanity = f.read().split("\n")


def loadSpamHamModel():
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    preprocessor = hub.KerasLayer("bert_models/bert-preprocessor")
    encoder_inputs = preprocessor(text_input)
    encoder = hub.KerasLayer("bert_models/bert-base", trainable=False)
    outputs = encoder(encoder_inputs)
    pooled_output = outputs["pooled_output"]  # [batch_size, 768].
    sequence_output = outputs["sequence_output"]  # [batch_size, seq_length, 768].

    fii = tf.keras.layers.Dropout(0.2, name="dropout")(pooled_output)
    fii = tf.keras.layers.Dense(64, activation="relu", name="hidden")(fii)
    fii = tf.keras.layers.Dense(32, activation="relu", name="hiddenn")(fii)
    fii = tf.keras.layers.Dense(8, activation="relu", name="hiddennn")(fii)
    fii = tf.keras.layers.Dense(1, activation="sigmoid", name="output")(fii)
    model = tf.keras.Model(inputs=[text_input], outputs=[fii])
    model.load_weights("models/spam_model_detection/spamhambert/model.weights.h5")
    return model


def loadPhishModel():
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    preprocessor = hub.KerasLayer("bert_models/bert-preprocessor")
    encoder_inputs = preprocessor(text_input)
    encoder = hub.KerasLayer("bert_models/tinybert", trainable=False)
    outputs = encoder(encoder_inputs)
    pooled_output = outputs["pooled_output"]  # [batch_size, 768].
    sequence_output = outputs["sequence_output"]  # [batch_size, seq_length, 768].

    fii = tf.keras.layers.Dropout(0.2, name="dropout")(pooled_output)
    # fii = tf.keras.layers.Dense(64, activation="relu", name="hidden")(fii)
    fii = tf.keras.layers.Dense(32, activation="relu", name="hiddenn")(fii)
    fii = tf.keras.layers.Dense(8, activation="relu", name="hiddennn")(fii)
    fii = tf.keras.layers.Dense(1, activation="sigmoid", name="output")(fii)
    model = tf.keras.Model(inputs=[text_input], outputs=[fii])
    model.load_weights(
        "models/phishing_model_detection/newphisingModel/model.weights.h5"
    )
    return model


spamHam_model = loadSpamHamModel()
phish_model = loadPhishModel()


def predict(messages: list[str]):
    is_spam_result = spamHam_model.predict([*messages])

    response = [
        {
            "message": messages[i],
            "is_spam": spam_result_decode(is_spam_result[i][0]),
            "has_profanity": has_profanityword(messages[i]),
            "links_found": [
                {"link": link, "isfraud_confidence": is_link_phish(link)}
                for link in findall_links(messages[i])
            ],
        }
        for i in range(len(messages))
    ]
    """[{
        "message"       : messages,             
        "is_spam"       : true | false,
        "has_profanity" : true | false, 
        "links_found"   : [
            {
                'link'  : link,
                'class' : "phish site" | "safe"
            },
            {
                'link'  : link,
                'class' : "phish site" | "safe"
            }
        ]
    },] """
    req = jsonify(response)
    # print(response)
    return req


def has_profanityword(message):
    words_arr = message.split(" ")
    for i in profanity:
        if i in words_arr:
            return True
    return False


def findall_links(message):
    result_links = URLExtract().find_urls(message)
    print("fraund links", result_links)
    return result_links


def spam_result_decode(result):
    if result >= 0.5:
        # print(result, True)
        return True
    else:
        # print(result, False)
        return False


def is_link_phish(message):
    result = phish_model.predict([filter_and_replace_punctuations(message)])[0][0]

    print(message, result)
    return float(result)


def filter_and_replace_punctuations(text):
    # Create a translation table to replace punctuations with spaces
    translation_table = str.maketrans(string.punctuation, " " * len(string.punctuation))

    # Use translate method
    filtered_text = text.translate(translation_table)

    # Alternatively, you can use the replace method
    # filtered_text = text.replace(string.punctuation, ' ' * len(string.punctuation))

    return filtered_text


@app.route("/",methods=["POST"])
def spam_check():
    json = request.json
    message = [*json["message"]]
    result = predict(message)
    return result


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)

# findall_links(
#     "introducing\ndoctor fucker - formulated\nhgh\nhuman growth hormone - also called hgh\nis referred to in medical science as the master hormone . it is \nwhen we are young , but near the age of twenty - one our bodies begin to produce\nless of it myxxxcocection.com/v1/js/jih321/l.popular.php by the time we are forty nearly everyone is deficient in hgh ,\nand at eighty our production has normally diminished at least 90 - 95 % . \nadvantages of hgh :\n- increased muscle strength\n- loss in body fat\n- increased bone density\n- lower blood pressure\n- quickens wound healing\n- reduces cellulite\n- improved vision\n- wrinkle disappearance\n- increased skin thickness texture\n- increased energy levels\n- improved sleep and emotional stability\n- improved memory and mental alertness\n- increased sexual potency\n- resistance to common illness\n- strengthened heart muscle\n- controlled cholesterol\n- controlled mood swings\n- new hair growth and color restore\nread\nmore at this website\nunsubscribe and visit this link www.myxxxcoection.com/v1/js/jih321/bpd.com.do/do/l.popular.php "
# )
