from .models import Tutorial, Reading_list
import random

def recommender(request):
    topic_list = ['প্রোগ্রামিং বাসিক', 'নাম্বার থিওরি', 'ডাটা স্ট্রাকচার', 'ডাইনামিক প্রোগ্রামিং', 'গ্রাফ থিওরি']

    tut_obj = Reading_list.objects.filter(user=request.user)

    qs = {}

    for i in topic_list:
        qs[i] = 0

    for tut in tut_obj:
        try:
            qs[tut.article.tag] += 1
        except:
            qs[tut.article.tag] = 1

    for key, val in qs.items():
        try:
            qs[key] = (val * 100) / Tutorial.objects.filter(tag=key).count()
            qs[key] = round(qs[key], 2)
        except:
            qs[key] = 0

        qs[key] += float(random.randint(1, 100))

    qs_sorted = sorted(qs.items(), key = lambda kv:(kv[1], kv[0]))

    suggestion = [' ', ' ']
    cnt = 0
    for key, val in qs_sorted:
        if cnt == 2:
            break

        done = [0, 0, 0, 0, 0, 0]
        try:
            tut_obj = Reading_list.objects.filter(user=request.user, article__tag=key).order_by('article__level')
            for tut in tut_obj:
                done[tut.article.level] = 1

        except:
            pass

        tut_obj = Tutorial.objects.filter(tag=key).order_by('level')

        for tut in tut_obj:
            if done[tut.level] == 0:
                suggestion[cnt] = (tut.title+' ('+key+')')
                cnt += 1
                break

    return suggestion


def parse(s):
    length = len(s)

    while s[length-1]!='(':
        length -= 1

    length -= 2

    s = s[:length]

    return s

def getID(tut):
    title = parse(tut)
    id = Tutorial.objects.filter(title=title).first().id

    return id