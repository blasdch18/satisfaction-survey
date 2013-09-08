{% load media %}
<link rel="stylesheet" href="{% media "jquery-ui-css/ui-lightness/jquery-ui.css" "no-timestamp" %}" type="text/css" media="all" />
<link rel="stylesheet" href="{% media "jquery.ui.stars.min.css" "no-timestamp" %}" type="text/css" media="all" />
<script type="text/javascript" src="{% media "jquery.js" "no-timestamp" %}"></script>
<script type="text/javascript" src="{% media "jquery-ui.js" "no-timestamp" %}"></script>
<script type="text/javascript" src="{% media "jquery.ui.stars.min.js" "no-timestamp" %}"></script>
<script type="text/javascript">
$(document).ready(function() {
    init();
});

var COMMENT_FROM = {{ comment_from }};
var MAX_RATE = {{ max_rate }};
</script>
<script type="text/javascript">{% block script %}{% endblock %}</script>
