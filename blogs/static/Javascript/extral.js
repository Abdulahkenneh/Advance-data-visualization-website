
    
        var textareas = document.getElementsByClassName('codemirror-textarea');
        for (var i = 0; i < textareas.length; i++) {
            CodeMirror.fromTextArea(textareas[i], {
                mode: 'markdown',
                theme: 'material',
                lineNumbers: true,
            });
        }
    

    
        document.addEventListener("DOMContentLoaded", function() {
            hljs.highlightAll();
        });
  



    
