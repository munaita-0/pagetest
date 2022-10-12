function writeToCookie() {
    document.cookie = "cookie_by_1st_js=aaaaaaaa;domain=hoge.js;secure";
}

function writeToLocalStorage() {
    localStorage.setItem('localstorage_by_1st_js', 'iiiiiiiiii');
}

writeToCookie()
writeToLocalStorage()

console.log('js_version_002')
  