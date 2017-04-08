window.onload = function(){
    var hour = 0;
    var mintue = 0;
    var second = 0;

    function timer(){

        second = second + 1;
        if(second >= 60){
            second = 0;
            mintue = mintue + 1;
        }

        if(mintue >= 60){
            mintue = 0;
            hour = hour + 1;
        }
        second = checkTime(second);
        mintue = checkTime(mintue);
        hour = checkTime(hour);

        document.getElementById("spendTimer").innerHTML = hour + ":" +mintue + ":" + second;
        second = second - 0;
        mintue = mintue - 0;
        hour = hour - 0;
    }

    var i = setInterval(timer,1000);
}

function checkTime(i)
{
    if (i<10) {
        i="0" + i
    }
    return i
}

function NumberCount(){
	var len = 120;
	var sLen = 0;
    var str = document.getElementById('textareaBox').value;
	var show = document.getElementById('totalNumber');
    try{
        //先将回车换行符做特殊处理
        str = str.replace(/(\r\n+|\s+|　+)/g,"龘");
        //处理英文字符数字，连续字母、数字、英文符号视为一个单词
        str = str.replace(/[\x00-\xff]/g,"m");  
        //合并字符m，连续字母、数字、英文符号视为一个单词
        str = str.replace(/m+/g,"*");
        //去掉回车换行符
        str = str.replace(/龘+/g,"");
        //返回字数
        sLen = str.length;
    }catch(e){
         
    }

    show.innerHTML = sLen;
    			
}

function showTips(){
    document.getElementById("tipsBox").style.display = "block";
}

function hideTips(){
    document.getElementById("tipsBox").style.display = "none";
}

function plan_back(){
//    window.history.back();
window.location.href = "../main";
}