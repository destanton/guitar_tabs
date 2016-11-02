from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.GET:
            base_url = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value={}'
            data = requests.get(base_url.format(self.request.GET.get("song_title")))
            parser = BeautifulSoup(data.text, "html.parser")
            results = parser.find_all("a")
            new_list = []
            for counter, tag in enumerate(results):
                if tag.get("href"):
                    new_list.append(tag.get("href"))

            # for song in new_list:
            #     song_link = song.replace("http://tabs.ultimate-guitar.com/", " ")
            #     print(song_link)
            context["song_link"] = new_list
        return context
