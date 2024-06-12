

  /**
 * 随机字符
 * @parm length     字符长度
 * @parm chars      随机的字符元素，传空值为：随机大小写字母加数字
 */
  const randomString = (length:any, chars:any) => {
    let c = chars
    if (!chars){c = '1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik9olQAZWSXEDCRFVTGBYHNUJMIKOLP'}
    let result = '';
    for (var i = length; i > 0; --i) result += c[Math.floor(Math.random() * c.length)];
    return result;
}

const getQueryVariable = (variable:string) =>
{
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    return(false);
}
const getQueryVariableHash = (variable:string) =>
{
    var vars = window.location.href.split('#')[0].split('&');
    console.info('jsutil vars',vars)
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    console.debug('jsutil.js  getQueryVariableHash:false ')
    return(false);
}
const getQueryVariableRoute = (variable:string) =>
{
    var vars = window.location.href.split('#')[1].split('&');
    console.info('jsutil vars',vars)
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    console.debug('jsutil.js  getQueryVariableHash:false ')
    return(false);
}

// 获取某天之后的日期
const getDateBefore = (curDate:any, subtractCount:any) => {
    let dd = new Date(curDate)
    dd.setDate(dd.getDate() - subtractCount) // 获取增加天数后的日期  
    let y = dd.getFullYear() 
    let m = (dd.getMonth() + 1) < 10 ? "0" + (dd.getMonth() + 1) : (dd.getMonth() + 1) //获取当前月份的日期，不足10补0  
    let d = dd.getDate() < 10 ? "0" + dd.getDate() : dd.getDate() //获取当前几号，不足10补0  
    return y + "-" + m + "-" + d
}

export {
    randomString, 
    getQueryVariable, 
    getQueryVariableHash,
    getQueryVariableRoute,
    getDateBefore
}