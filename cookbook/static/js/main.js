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
    
    $('.collapsible').collapsible();
    
    $('select').formSelect();
    
    $('.modal').modal();
    
    $('input#recipe_title').characterCounter();
    
    
    $('.box .title').matchHeight();
    $('.box .info').matchHeight();
    $('.box .desc-body').matchHeight();
    
  });
    