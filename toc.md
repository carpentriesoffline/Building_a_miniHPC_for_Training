---
layout: default
title: Table of Contents
---

{% for entry in site.data.toc %}
<div class="toc-page">
  <h2><a href="{{ site.baseurl }}/{{ entry.link }}">{{ entry.title }}</a></h2>
  {% if entry.headings.size > 0 %}
  <ul class="toc-sections">
    {% for heading in entry.headings %}
    <li class="toc-level-{{ heading.level }}">
      <a href="{{ site.baseurl }}/{{ entry.link }}#{{ heading.anchor }}">{{ heading.title }}</a>
    </li>
    {% endfor %}
  </ul>
  {% endif %}
</div>
{% endfor %}
