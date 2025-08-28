import json
from django.http import HttpResponse
from apps.bot.misc import get_dispatcher_and_bot, get_or_create_event_loop


def process_update(request, token: str):
    try:
        dp, bot = get_dispatcher_and_bot()
        if token == bot.token:
            body_unicode = request.body.decode('utf-8')
            update = json.loads(body_unicode)
            loop = get_or_create_event_loop()
            loop.run_until_complete(dp.feed_raw_update(bot, update))
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    except Exception as e:
        print(f"Bot update error: {e}")
        return HttpResponse(status=500)


process_update.csrf_exempt = True
