var xOs = 5;
var yOS = 5;
var xP = 400;
var yP = -100;
var canRun = 1;

async function flipFace(){
    img1 = document.getElementById("image1");
    img2 = document.getElementById("image2");
    img3 = document.getElementById("image3");
    words = document.getElementById("words");
    while(true){
        document.getElementById("idiot").play();
        img1.src = "face2.png"
        img2.src = "face2.png"
        img3.src = "face2.png"
        document.body.style.background = "black";
        words.style.color = "white";
        await delay(350);
        img1.src = "face1.png"
        img2.src = "face1.png"
        img3.src = "face1.png"
        document.body.style.background = "white";
        words.style.color = "black";
        await delay(350);
    }
}

function delay(milliseconds){
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}

function spawn() {
    openWindow(document.URL);
    
}
  
function dblspawn() {spawn(); spawn();}

function openWindow(url) {
    window.open(url, "_blank", 'menubar=no, status=no, toolbar=no, resizable=no, width=350, height=400, titlebar=no, alwaysRaised=yes');
}

//animations
function posXleft() {
    xOs = Math.ceil(-6 * Math.random()) * 5 - 10;
    window.focus()
}
  
function posXright() {
    xOs = Math.ceil(7 * Math.random()) * 5 - 10;
}
  
function posYup() {
    yOS = Math.ceil(-6 * Math.random()) * 5 - 10;
}
  
function posYdown() {
    yOS = Math.ceil(7 * Math.random()) * 5 - 10;
}
  
  
function anim() {
    xP += xOs;
    yP += yOS;
  
    if (xP > screen.width - 357) {
      posXleft();
    }
  
    if (xP < 0) {
      posXright();
    }
  
    if (yP > screen.height - 330) {
      posYup();
    }
  
    if (yP < 0) {
      posYdown();
    }
  
    if (canRun == 1) {
      window.moveTo(xP, yP);
      setTimeout('anim()', 1);
    }
}