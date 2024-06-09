tinymce.init({
    selector: 'textarea',
    min_height: 350,
     skin: "oxide",
     icons: 'material' ,
   preview_styles: 'font-size color',
    resize: 'both',
    plugins: 'link image media code autolink lists media table',
    toolbar: 'undo redo | styleselect| forecolor  | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | link image media| code table',
    toolbar_mode: 'floating',
     /* enable title field in the Image dialog*/
    image_title: true,
    /* enable automatic uploads of images represented by blob or data URIs*/automatic_uploads: true,images_upload_url: 'postAcceptor.php',file_picker_types: 'image',
  
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name'
    
  });