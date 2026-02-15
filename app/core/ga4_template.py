import os

GA4_MEASUREMENT_ID = os.environ.get("GA4_MEASUREMENT_ID", "G-DEVELOPMENT")

GA4_SNIPPET = """<!-- Stardance GA4 Attribution Layer (PTC-production) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', '{measurement_id}', { send_page_view: false });

  (function () {
    var params = new URLSearchParams(window.location.search);
    var hubMeta = {
      hub_id: document.body.getAttribute('data-hub-id') || 'unknown',
      allocation_id: params.get('utm_content') || 'direct',
      brand_id: params.get('utm_term') || 'unknown',
      campaign_id: params.get('utm_campaign') || 'unknown',
      utm_source: params.get('utm_source') || 'direct',
      utm_medium: params.get('utm_medium') || 'none'
    };

    gtag('event', 'hub_page_view', hubMeta);

    function sendEventThenNavigate(eventName, eventParams, navigateFn) {
      var done = false;
      function finish() {
        if (done) return;
        done = true;
        if (typeof navigateFn === 'function') navigateFn();
      }
      var timer = setTimeout(finish, 250);
      try {
        gtag('event', eventName, Object.assign({}, eventParams, {
          event_callback: function () { clearTimeout(timer); finish(); }
        }));
      } catch (e) { clearTimeout(timer); finish(); }
    }

    document.addEventListener('DOMContentLoaded', function () {
      var video = document.querySelector('video');
      if (video) {
        var firedVideo = false;
        var playTimer = null;
        function clearPlayTimer() { if (playTimer) { clearTimeout(playTimer); playTimer = null; } }
        video.addEventListener('play', function () {
          if (firedVideo) return;
          clearPlayTimer();
          playTimer = setTimeout(function () {
            if (firedVideo) return;
            firedVideo = true;
            gtag('event', 'hub_video_play', Object.assign({}, hubMeta, {
              video_duration: Math.round(video.duration || 0)
            }));
          }, 2000);
        });
        video.addEventListener('pause', clearPlayTimer);
        video.addEventListener('ended', clearPlayTimer);
      }

      var form = document.querySelector('form[data-capture="email"]');
      if (form) {
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          sendEventThenNavigate('hub_email_capture', hubMeta, function () { form.submit(); });
        });
      }

      document.querySelectorAll('a[data-affiliate="true"]').forEach(function (link) {
        link.addEventListener('click', function (e) {
          if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || link.target === '_blank') return;
          e.preventDefault();
          var destination = link.href || '';
          sendEventThenNavigate(
            'hub_affiliate_click',
            Object.assign({}, hubMeta, { destination_url: destination }),
            function () { window.location.href = destination; }
          );
        });
      });

    });
  })();
</script>"""

def get_ga4_snippet(measurement_id: str = GA4_MEASUREMENT_ID) -> str:
    return GA4_SNIPPET.format(measurement_id=measurement_id)
