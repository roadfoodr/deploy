from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.conf import settings
import os, json, logging
import folium
from django.views.generic import TemplateView

from rftrackr.models import User, Roadfood, Visit

HARDWIRED_USER_ID = 2
HARDWIRED_USER = User.objects.get(pk=HARDWIRED_USER_ID)


def index(request):
    return render(request, 'index.html')
def testpage(request):
    return render(request, 'testpage.html')

# view for /map
class FoliumView(TemplateView):
    template_name = "rftracker/map.html"

    def get_context_data(self, **kwargs):
        # Was a keyword argument (roadfood to be toggled) passed in?
        if (rf_id := self.request.GET.get('rf_id', None)):
            # print(f'Got {rf_id=}', flush=True)
            clicked_rf = Roadfood.objects.get(pk=rf_id)
            center_latlong = [clicked_rf.lat, clicked_rf.long]

            # "toggle" the visit status of this roadfood by creating or deleting a Visit
            v = Visit.objects.filter(
                    user_id=HARDWIRED_USER,
                    rf_id=clicked_rf
                    )
            if v:
                v.delete()
            else:
                v = Visit(
                    user_id=HARDWIRED_USER,
                    rf_id=clicked_rf,
                    # visit_date=now
                    )
                v.save()
        else:
            # default center -- could compute instead from current selection of rfs
            center_latlong = [38.038121, -78.484627]

        # set up the map, layers, and markers
        figure = folium.Figure()
        m = folium.Map(
            location=center_latlong,
            zoom_start=14,
            tiles=None
        )
        m.add_to(figure)

        folium.TileLayer(tiles='Stamen Toner', control=False).add_to(m)

        (map_layer_visited := folium.FeatureGroup(name='Visited')).add_to(m)
        (map_layer_unvisited := folium.FeatureGroup(name='Not visited... yet')).add_to(m)


        visited = Visit.objects.filter(user_id=HARDWIRED_USER)
        # Certainly there must be a better way to query these
        visited_rfs = [v.rf_id for v in visited]

        rfs = Roadfood.objects.all()
        for rf in rfs:
            if rf in visited_rfs:
                folium.Marker(
                    location=[rf.lat, rf.long],
                    popup=f'<a href=/map?rf_id={rf.rf_id}>{rf.name}</a>',
                    icon=folium.Icon(color='red', icon='ok-sign')
                ).add_to(map_layer_visited)
            else:
                folium.Marker(
                    location=[rf.lat, rf.long],
                    popup=f'<a href=/map?rf_id={rf.rf_id}>{rf.name}</a>',
                    icon=folium.Icon(color='blue', icon='cutlery')
                ).add_to(map_layer_unvisited)

        folium.LayerControl(collapsed=False).add_to(m)

        figure.render()
        return {"map": figure}