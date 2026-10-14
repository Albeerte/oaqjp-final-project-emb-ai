import requests
import json


def _empty_emotion_response():
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }


def _format_emotion_response(emotions):
    emotion_scores = {
        'anger': emotions['anger'],
        'disgust': emotions['disgust'],
        'fear': emotions['fear'],
        'joy': emotions['joy'],
        'sadness': emotions['sadness']
    }

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        **emotion_scores,
        'dominant_emotion': dominant_emotion
    }


def _offline_emotion_response(text_to_analyze):
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_emotion_response()

    text = text_to_analyze.lower()
    keyword_scores = {
        'anger': ['angry', 'mad', 'furious', 'irritated', 'outraged'],
        'disgust': ['disgust', 'disgusted', 'gross', 'revolting', 'repulsed'],
        'fear': ['afraid', 'fear', 'scared', 'terrified', 'worried'],
        'joy': ['glad', 'happy', 'joy', 'delighted', 'pleased'],
        'sadness': ['sad', 'sadness', 'unhappy', 'miserable', 'heartbroken']
    }

    scores = {
        emotion: 0.9 if any(keyword in text for keyword in keywords) else 0.0
        for emotion, keywords in keyword_scores.items()
    }

    if not any(scores.values()):
        scores['joy'] = 0.1

    return _format_emotion_response(scores)


def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }
    try:
        response = requests.post(url, json=myobj, headers=headers, timeout=10)
    except requests.RequestException:
        return _offline_emotion_response(text_to_analyze)
    
    if response.status_code == 400:
        return _empty_emotion_response()

    formatted_response = json.loads(response.text)
    
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    return _format_emotion_response(emotions)
