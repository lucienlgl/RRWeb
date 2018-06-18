from rrsite.models import Photo


def get_cover(restaurant_id):
    cover_id = list(Photo.objects.filter(restaurant_id=restaurant_id).values('id')[:1])
    if cover_id:
        return cover_id[0]['id']
    else:
        return None
