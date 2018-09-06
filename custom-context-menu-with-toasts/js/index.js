document.addEventListener('contextmenu', event => {event.preventDefault();showCtxMenu(event.clientX,event.clientY);});

document.addEventListener("DOMContentLoaded", demo);

var menuHeight = 200;
var menuWidth = 150;
var menuItemH = 40;
var submMenuHGap = menuItemH*3;

function showCtxMenu(mouseX,mouseY){
  removeCtxMenu();
  var curX = mouseX+'px';
  var curY = mouseY+'px';
  var curSubX = mouseX+'px';
  var curSubY = mouseY+'px';
  var test = document.createElement('div');
  test.innerHTML = 
  '<div id="menu">'+
    '<ul>'+
     ' <li id="fstItem">@oneplusuniverse</li>'+
      '<li id="scdItem">Second Item</li>'+
      '<li id="thrItem">Third Item</li>'+
      '<li id="frtItem">Fourth Item</li>'+
        '<div class="subMenu">'+
          '<ul>'+
            '<li id="fstSubItem">First SubItem</li>'+
            '<li id="scdSubItem">Second SubItem</li>'+
            '<li id="thrSubItem">Third SubItem</li>'+
            '<li id="frtSubItem">Fourth SubItem</li>'+
          '</ul>'+
        '</div>'+
      '<li id="fftItem">Fifth Item</li>'+
    '</ul>'+
  '</div>';
  
  test.classList.add("ctxMenu");
  
  if(mouseY<menuHeight){
    curY = mouseY;
    }else{
    curY = mouseY-menuHeight;
  }
  if((window.innerWidth-mouseX)<menuWidth){
    curX = mouseX-menuWidth;
    test.classList.add("revCtxMenu");
    }else{
      curX = mouseX;
    }
  
  test.style.top = curY+'px';
  test.style.left = curX+'px';
  document.body.appendChild(test);
  var sbmnTrigger = document.getElementById('frtItem');
  var submenu = document.getElementsByClassName('subMenu')[0];

  if((window.innerHeight - mouseY)<submMenuHGap){
    curSubY = (submMenuHGap-40)-((mouseY+submMenuHGap)-window.innerHeight);
  }else{
    curSubY=submMenuHGap;
  }
  if((window.innerWidth-mouseX)<menuWidth*2){
    curSubX = -menuWidth;
    // test.classList.add("revCtxMenu");
    }else{
      curSubX = menuWidth;
    }
  
  submenu.style.top=curSubY+'px';
  submenu.style.left=curSubX+'px';
  
  sbmnTrigger.onmouseover = function(){submenu.style.display='block';};
  submenu.onmouseover = function(){submenu.style.display='block';};
  sbmnTrigger.onmouseout = function(){submenu.style.display='none';};
  submenu.onmouseout = function(){submenu.style.display='none';};
}

function toast(msg){
  if(document.getElementsByClassName('toastwrp')[0]){
    document.body.removeChild(document.getElementsByClassName('toastwrp')[0]);
  }
  var toast = document.createElement('div');
  toast.innerHTML = 
  // '<div class="toastwrp">'+
    '<div id="toast" class="toast">'+
      msg+
    '</div>';//+
  // '</div>';
  var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
  toast.classList.add("toastwrp");
  document.body.appendChild(toast);
  toast.style.left = ((w/2)-(document.getElementsByClassName('toast')[0].offsetWidth/2))+'px';
  setTimeout(function() {document.body.removeChild(document.getElementsByClassName('toastwrp')[0]);}, 1000)
}

function removeCtxMenu(){
  if(document.getElementsByClassName('ctxMenu')[0]){
    document.body.removeChild(document.getElementsByClassName('ctxMenu')[0]);
  }
  
}

function detectClick(e) {
  switch (e.target.id) {
    case('fstItem'): 
      openInNewTab('https://codepen.io/oneplusuniverse/');
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('scdItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('thrItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('frtItem'): 
      break;
    case('fftItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('fstSubItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('scdSubItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('thrSubItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('frtSubItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    case('fftSubItem'): 
      toast(document.getElementById(e.target.id).innerHTML);
      removeCtxMenu();
      break;
    default:
      removeCtxMenu();
      break;
  }
    
}

function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}


function demo(){
  var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
  var element = document.getElementsByTagName("BODY")[0];
  var e = element.ownerDocument.createEvent('MouseEvents');
  e.initMouseEvent('contextmenu', true, true,
     showCtxMenu(w/2-75,h-100), 1, 0, 0, 0, 0, false,
     false, false, false,2, null);
  
  var first = document.getElementById('fstItem');
  var second = document.getElementById('scdItem');
  var third = document.getElementById('thrItem');
  var fourth = document.getElementById('frtItem');
  
  setTimeout(function(){
   first.classList.add("demoHover");
  },600);
  
  setTimeout(function(){
    first.classList.remove("demoHover");
   second.classList.add("demoHover");
  },1000);
  
  setTimeout(function(){
    second.classList.remove("demoHover");
   third.classList.add("demoHover");
  },1100);
  
  setTimeout(function(){
    third.classList.remove("demoHover");
   // fourth.classList.add("demoHover");
  },1300);
}

// demo();

 window.onresize = function(e) {
   removeCtxMenu();
 };
document.addEventListener("click", detectClick, false);