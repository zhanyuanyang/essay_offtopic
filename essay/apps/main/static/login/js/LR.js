window.onload = function(){
	var Bhead = document.getElementById("Boxhead");
	var hLi = Bhead.getElementsByTagName("Li");
	var LRDiv = document.getElementById("LoginResgi");
	var hDiv = LRDiv.getElementsByTagName("div");
	for(var i = 0;i < hLi.length ;i++){
		hLi[i].index = i;
		hLi[i].onclick = function(){
			for(var i=0; i < hLi.length;i++){
				hLi[i].className = "";
			}
			this.className = "active";
			for(var j = 0;j < hDiv.length; j++){
				hDiv[j].className = "hide";
			}
			hDiv[this.index].className = "show";
		}
	}
}