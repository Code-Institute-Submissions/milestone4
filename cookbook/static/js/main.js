  $(document).ready(function() {
    $('.sidenav').sidenav({
      draggable: true,
      preventScrolling: true,
    });

    $('.slider.home-slider').slider({
      indicators: false,
      height: 600,
    });
    
    $('.slider.inner-slider').slider({
      indicators: false,
      height: 300,
    });
    
    $('select').formSelect();
    
    $('.modal').modal();
    
    $('input#recipe_title').characterCounter();
    
  });
    