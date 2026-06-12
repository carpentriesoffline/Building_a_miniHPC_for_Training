---
layout: default
title: Table of Contents
---

{% for page in site.data.toc %}
<div class="toc-page">
  <h2><a href="{{ site.baseurl }}/{{ page.link }}">{{ page.title }}</a></h2>
  {% if page.headings.size > 0 %}
  <ul class="toc-sections">
    {% for heading in page.headings %}
    <li class="toc-level-{{ heading.level }}">
      <a href="{{ site.baseurl }}/{{ page.link }}#{{ heading.anchor }}">{{ heading.title }}</a>
    </li>
    {% endfor %}
  </ul>
  {% endif %}
</div>
{% endfor %}
