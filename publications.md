---
layout: single
title: "Publications"
permalink: /publications/
---

{% assign pubs_by_year = site.data.publications | group_by: "year" %}

{% for year_group in pubs_by_year %}
## {{ year_group.name }}

{% for p in year_group.items %}
<p>
  {% if p.authors != "" %}{{ p.authors }}. {% endif %}
  {% if p.year != "" %}({{ p.year }}). {% endif %}
  {% if p.title != "" %}{{ p.title }}. {% endif %}
  {% if p.journal != "" %}<em>{{ p.journal }}</em>{% endif %}
  {% if p.volume != "" %}, <em>{{ p.volume }}</em>{% endif %}
  {% if p.issue != "" %}({{ p.issue }}){% endif %}
  {% if p.pages != "" %}, {{ p.pages }}{% endif %}.
  {% if p.doi != "" %}<a href="https://doi.org/{{ p.doi }}">https://doi.org/{{ p.doi }}</a>{% endif %}
</p>
{% endfor %}

{% endfor %}
