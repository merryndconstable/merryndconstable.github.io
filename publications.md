---
layout: single
title: "Publications"
permalink: /publications/
---

{% assign pubs = site.data.publications %}

{% for p in pubs %}

**{{ p.title }}** ({{ p.year }})

{% if p.doi != "" %}
DOI: https://doi.org/{{ p.doi }}
{% endif %}

{% endfor %}
