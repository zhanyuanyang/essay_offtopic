function showSelection(){
	document.getElementById("showT").style.display = "none";
	document.getElementById("showS").style.display = "inline-block";
}

function showText(){
	document.getElementById("showT").style.display = "inline-block";
	document.getElementById("showS").style.display = "none";
}

//修改个人信息弹窗
function showPhoto(){
	document.getElementById('hidebg').style.display = 'block';
	var myObject = document.getElementById('tmodify');
	myObject.style.display = "block";
}
//隐藏个人信息弹窗
function hidePhoto(){
	document.getElementById('hidebg').style.display = 'none';
	var myObject = document.getElementById('tmodify');
	myObject.style.display = "none";
}

function showtmodifyPsw(){
	var modifyTable = document.getElementById('tmodifyTable');
	var tr = modifyTable.getElementsByTagName("tr");
	for(var i = 3;i<6;i++){
		tr[i].style.display = "block";
		tr[i].style.width = "420px";
		tr[i].style.marginBottom = "10px";
	}

}