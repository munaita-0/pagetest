function writeToCookie() {
    max_age = 60 * 60 * 24 * 1000
    document.cookie = "1st_with_secure=iiii;Secure;max-age=" + max_age;
    document.cookie = "1st_with_write_domain=uuuu;domain=ones-form-test.55-inc.jp;max-age=" + max_age;
    document.cookie = "1st_with_wrong_domain=uuuu;domain=hoge.jp";
}

function writeToLocalStorage() {
    localStorage.setItem('localstorage_by_1st_js', 'iiiiiiiiii');
}

writeToCookie()
writeToLocalStorage()

console.log('js_version_005')
  