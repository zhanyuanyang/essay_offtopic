window.onload = function(){
	var Bhead = document.getElementById("RContainerHead");
	var hLi = Bhead.getElementsByTagName("Li");
	var kuangOne = document.getElementById("total_chart");
	var kuangTwo = document.getElementById("detail_error");
	for(var i = 0;i < hLi.length ;i++){
		hLi[i].index = i;
		hLi[i].onclick = function(){
			for(var i=0; i < hLi.length;i++){
				hLi[i].className = "";
			}
			this.className = "active";
			if(this.index == 0){
				kuangOne.style.display = "block";
				kuangTwo.style.display = "none";
				clearErrorBox();
			}else if(this.index == 1){
				kuangOne.style.display = "none";
				kuangTwo.style.display = "block";
				showErrorBox();
			}
			
		}
	}

    var json = {}
    json.errors = errors;
    json.content = content;

	var textarea = document.getElementById('formertext');
	textarea.innerHTML = content.content;

	var magicArray = textarea.innerHTML.split("");
	for(var i = 0;i<magicArray.length;i++){
		var magic_span = document.createElement("span");
		magic_span.id = "magic"+i;
		magic_span.innerHTML = magicArray[i];
		document.getElementById("showMagic").appendChild(magic_span);
	}
for(var i = 0;i<errors.length;i++){


//	var rDiv = document.createElement('div');
//    var stringtest = errors[i].replace_word;
//	var stringArray = stringtest.split(",");
//	!function(i){
//	for(var c=errors[i].index.start ; c <= errors[i].index.end ; c++)
//		document.getElementById("magic"+c).onmouseover = function(){
//			rDiv.className = "replaceWord";
////			rDiv.innerHTML = "<p>" + errors[i].error_type +"错误："+ "</p >" +"<span>" + errors[i].replace_word + "</span>";
//            rDiv.innerHTML = "<p>" + errors[i].error_type +"错误："+ "</p >";
//            rDiv.innerHTML +="<span>" + errors[i].replace_word + "</span>";
//			document.getElementById("showMagic").appendChild(rDiv);
//
//		}
//	}(i);//闭包问题

    var rDiv = document.createElement('div');
	//修改
	var stringArray = errors[i].replace_word;
	console.log(stringArray);
//	var stringArray = stringtest.split(",");
	//修改END
	!function(i){
	for(var c=errors[i].index.start ; c <= errors[i].index.end ; c++){
		document.getElementById("magic"+c).onmouseover = function(){
			rDiv.className = "replaceWord";
			rDiv.innerHTML = "<p>" + errors[i].error_type +"错误："+ "</p >" ;
			if(stringArray.length>=5){
				for(var t=0;t<3;t++){
					rDiv.innerHTML += "<span>" + errors[i].replace_word[t] + "</span>";
				}
			}
			else{
				for(var t = 0;t<stringArray.length;t++){
					rDiv.innerHTML += "<span>" + errors[i].replace_word[t]+ "</span>";
				}
			}

			document.getElementById("showMagic").appendChild(rDiv);

		}
		}
	}(i);//闭包问题



	!function(i){
	for(var c=errors[i].index.start ; c <= errors[i].index.end ; c++){

			document.getElementById("magic"+c).onmouseout = function(){
		        rDiv.className = "hide";

	}

		}
	}(i);//闭包问题





	switch(errors[i].error_type){
	case'名词':{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "red";
		}
		break;
	}
	case'副词':{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "yellow";
		}
		break;
	}
	case'动词':{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "blue";
		}
		break;
	}
	case'形容词':{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "pink";
		}
		break;
	}
	case'连词':{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "green";
		}
		break;
	}
	case'介词':{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "orange";
		}
		break;
	}
	default:{
		for(var j =errors[i].index.start ;j<=errors[i].index.end;j++){
			document.getElementById("magic" + j).className = "orange";
		}
	}
}
}



}



function result_back(){
	window.history.back(-1);
}

function showErrorBox(){
	json = {}
//	var detail = {{ detail|safe }};
    json.detail = detail
	var error_table = document.getElementById('error_table');
	for(var i = 0;i<detail.length;i++){
		var newTr = error_table.insertRow();
		var newTd0 = newTr.insertCell();
		var newTd1 = newTr.insertCell();
		var newTd2 = newTr.insertCell();
		 newTd0.innerHTML = i+1;
		 newTd1.innerHTML = detail[i].位置;
		 newTd2.innerHTML = detail[i].提示;
	}
}

function clearErrorBox(){
	var error_table = document.getElementById('error_table');
	while(error_table.hasChildNodes()) //当div下还存在子节点时 循环继续  
    {  
        error_table.removeChild(error_table.firstChild);  
    } 
}
