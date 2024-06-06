
    $(document).ready(function() {
      $('#your_summernote_id').summernote({
        height: 300,
          // Set editor height
        callbacks: {
          onInit: function() {
            // Apply the custom CSS
            $('.note-editable').css({
              'white-space': 'pre-wrap',
              'word-wrap': 'break-word',
              'overflow-x': 'auto',
              'max-width': '100%'
            });
            $('.note-editable img').css({
              'max-width': '100%',
              'height': 'auto',
              'display': 'block'
            });
          }
        }
      });
    });
   