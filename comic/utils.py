import wakatime

def get_wakatime_stats(api_key):
    wakatime_api = wakatime.ApiClient(api_key)
    user_stats = wakatime_api.get_user_stats()

    return user_stats['data']['human_readable_daily_average']
