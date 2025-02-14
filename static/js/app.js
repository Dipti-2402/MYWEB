const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');
const bars = document.querySelectorAll(' .bar');
  menu.addEventListener('click',function()
{
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active');

    bars.forEach(bar => 
    {
      bar.classList.toggle('active');
    });
});
