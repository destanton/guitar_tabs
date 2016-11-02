from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup


class SongView(TemplateView):
    template_name = "song.html"

    def get_context_data(self, song_link):
        context = super().get_context_data()
        page = requests.get("https://tabs.ultimate-guitar.com/" + song_link)
        parser = BeautifulSoup(page.text, "html.parser")
        context["chords"] = parser.find_all(id="cont")
        print(context)
        return context


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
            for song in results:
                if song.get("class") == ["song", "result-link"]:
                    song_link = song.get("href").replace("https://tabs.ultimate-guitar.com/", "")
                    new_list.append((song_link, song.get_text()))
            print(new_list)
            # for song in new_list:
            #     song_link = song.get("href).replace("http://tabs.ultimate-guitar.com/", " ")
            #     print(song_link)
            context["song_links"] = new_list
        return context
