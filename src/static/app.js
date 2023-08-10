const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

const periksa = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add('show');
        }
    });
});

const upcomingObject = document.querySelectorAll('.upcoming,.fog,.upcominggg');
upcomingObject.forEach((el) => observer.observe(el));

const onceObject = document.querySelectorAll('.upcoming-once,.upcomingX');
onceObject.forEach((el) => periksa.observe(el));

window.onscroll = function() {myFunction()};

var header = document.getElementById("myHeader");
var sticky = document.getElementById("sticky");
var active = document.getElementById("active");
var subMenu = document.getElementById("subMenu");
var prof = document.getElementById("user-prof");
var sticky = header.offsetTop;

function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
    header.classList.add("active");
  } else {
    header.classList.remove("sticky");
    header.classList.remove("active");
  }
}

let processScroll = () => {
    let docElem = document.documentElement, 
        docBody = document.body,
        scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
        scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - window.innerHeight,
        scrollPercent = scrollTop / scrollBottom * 100 + '%';
    
    // console.log(scrollTop + ' / ' + scrollBottom + ' / ' + scrollPercent);
    
    document.getElementById("progress-bar").style.setProperty("--scrollAmount", scrollPercent); 
}

document.addEventListener('scroll', processScroll);

function toggleMenu(){
    subMenu.classList.toggle("open-menu");
    prof.classList.toggle("background");
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
